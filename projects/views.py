# projects/views.py
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.module_loading import import_string
from .models import Stand
from .stands.proxy import proxy_to_upstream

def _user_in_group(user, group_name: str) -> bool:
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True
    if not group_name:
        return False
    return user.groups.filter(name=group_name).exists()

@login_required(login_url='/accounts/login/')
def stand_detail(request, slug):
    stand = get_object_or_404(Stand, slug=slug, is_active=True)
    if not _user_in_group(request.user, stand.group_name):
        return render(request, "projects/stand_detail.html", {"stand": stand, "has_access": False}, status=403)

    if stand.source == "external" and stand.upstream_url:
        return proxy_to_upstream(request, stand.upstream_url)

    if stand.source == "internal" and stand.view_path:
        view_func = import_string(stand.view_path)
        return view_func(request)
