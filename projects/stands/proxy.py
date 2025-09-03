import requests
from urllib.parse import urljoin, urlparse
from django.http import StreamingHttpResponse, HttpResponse

SIGN_HEADER = "X-Stand-Signature"

HOP_BY_HOP = {
    "connection", "keep-alive", "proxy-authenticate", "proxy-authorization",
    "te", "trailers", "transfer-encoding", "upgrade",
}
EXCLUDE_DOWN_HEADERS = { *HOP_BY_HOP, "server", "x-powered-by", "x-frame-options" }

def _build_target_url(base: str, subpath: str) -> str:
    return urljoin(base.rstrip('/') + '/', subpath)

def _clean_headers_down(headers: requests.structures.CaseInsensitiveDict) -> dict:
    out = {}
    for k, v in headers.items():
        if k.lower() in EXCLUDE_DOWN_HEADERS:
            continue
        out[k] = v
    return out

def _inject_base_marker(html: str, mount_prefix: str) -> str:
    import re
    head_re = re.compile(r"(<head[^>]*>)", re.IGNORECASE)
    base_re = re.compile(r"<base\s+href=['\"][^'\"]*['\"][^>]*>", re.IGNORECASE)
    if base_re.search(html):
        html = base_re.sub(f'<base href="{mount_prefix}">', html, count=1)
    else:
        html = head_re.sub(rf'\1\n<base href="{mount_prefix}">', html, count=1)
    return html.replace("</head>", '<!-- PROXY:BASE-INJECTED -->\n</head>', 1)

def _rewrite_prefixes(text: str, upstream_base: str, mount_prefix: str) -> str:
    up = urlparse(upstream_base)
    path = up.path or "/"
    full = f"{up.scheme}://{up.netloc}{path}"
    for needle in (full, full.rstrip("/")):
        text = text.replace(needle, mount_prefix.rstrip("/"))
    proto_rel = f"//{up.netloc}{path}"
    for needle in (proto_rel, proto_rel.rstrip("/")):
        text = text.replace(needle, mount_prefix.rstrip("/"))
    if path and path != "/":
        for needle in (path, path.rstrip("/")):
            text = text.replace(needle, mount_prefix.rstrip("/"))
    return text

def proxy_to_upstream(
    request,
    upstream_base_url: str,
    *,
    subpath: str = "",
    signature: str | None = None,
    mount_prefix: str = "/",
):
    if not upstream_base_url:
        return HttpResponse("Upstream is not configured", status=500)

    target_url = _build_target_url(upstream_base_url, subpath)
    headers_up = {
        "X-Forwarded-Proto": "https" if request.is_secure() else "http",
        "X-Forwarded-For": request.META.get("REMOTE_ADDR", ""),
        "Host": urlparse(upstream_base_url).netloc,
        "Accept-Encoding": "identity",
    }
    if signature:
        headers_up[SIGN_HEADER] = signature

    data = request.body if request.method in ("POST", "PUT", "PATCH") else None
    params = request.GET.copy()

    try:
        resp = requests.request(
            request.method, target_url,
            headers=headers_up, params=params, data=data,
            stream=False, timeout=30,
        )
    except requests.RequestException as e:
        return HttpResponse(f"Upstream error: {e}", status=502)

    if resp.status_code == 404 and subpath and not any(
        subpath.endswith(ext) for ext in (".js", ".css", ".png", ".jpg", ".jpeg",
                                          ".svg", ".json", ".map", ".ico",
                                          ".woff", ".woff2", ".ttf", ".mp4")
    ):
        try:
            resp = requests.get(_build_target_url(upstream_base_url, ""), headers=headers_up, params=params, timeout=15)
        except requests.RequestException as e:
            return HttpResponse(f"Upstream error: {e}", status=502)

    content_type = resp.headers.get("Content-Type", "").lower()
    body = resp.content

    is_html = ("text/html" in content_type) or body.strip().lower().startswith(b"<!doctype html") or b"<html" in body[:4096]
    if is_html:
        text = body.decode("utf-8", errors="ignore")
        text = _inject_base_marker(text, mount_prefix)
        text = _rewrite_prefixes(text, upstream_base_url, mount_prefix)
        body = text.encode("utf-8", errors="ignore")

    dj = HttpResponse(body, status=resp.status_code)
    for k, v in _clean_headers_down(resp.headers).items():
        if k.lower() == "content-length":
            continue
        dj[k] = v
    dj["X-Frame-Options"] = "SAMEORIGIN"
    return dj
