from projects.models import Stand

def menu_items(request):
    items = [{"title": "Главная", "url": "/", "locked": False}]
    u = request.user
    for stand in Stand.objects.filter(is_active=True).order_by("title"):
        url = f"/projects/{stand.slug}/"
        has_access = (
            u.is_authenticated and
            (u.is_superuser or u.groups.filter(name=stand.group_name).exists())
        )
        items.append({"title": stand.title, "url": url, "locked": not has_access})
    if not u.is_authenticated:
        items.append({"title": "Sign in", "url": "/accounts/login/", "locked": False})
    return {"menu_items": items}
