from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from ...models import Stand
from ..proxy import proxy_to_upstream

def _user_in_group(user, group_name: str) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not group_name:
        return False
    return user.groups.filter(name=group_name).exists()

@login_required
def entry(request, subpath: str = ""):
    stand = get_object_or_404(Stand, slug="sofclab", is_active=True)
    if not _user_in_group(request.user, stand.group_name):
        return render(request, "projects/stand_detail.html", {"stand": stand, "has_access": False}, status=403)
    return proxy_to_upstream(request, stand.upstream_url, subpath=subpath, mount_prefix="/projects/sofclab/")

