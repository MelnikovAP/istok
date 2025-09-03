from django.urls import path, re_path
from . import views

app_name = "h2race"

urlpatterns = [
    path("", views.entry, name="root"),
    re_path(r"^(?P<subpath>.*)$", views.entry, name="proxy"),
]
