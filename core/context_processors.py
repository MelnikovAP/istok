from django.urls import reverse

def menu_items(request):
    """
    Возвращает список пунктов меню для боковой панели
    в зависимости от статуса и прав пользователя.
    """
    items = [
        {
            "title": "Main",
            "url": reverse("home"),
        }
    ]

    if request.user.is_authenticated:
        items.append({
            "title": "Projects",
            "url": reverse("project_list"),
        })

        if request.user.is_staff:
            items.append({
                "title": "Admin panel",
                "url": reverse("admin:index"),
            })
    else:

        items.append({
            "title": "Sign In",
            "url": reverse("account_login"),
        })

    return {
        "menu_items": items
    }
