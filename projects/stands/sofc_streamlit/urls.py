from django.urls import path, re_path
from . import views

app_name = "sofc_streamlit"

urlpatterns = [
    path("", views.entry, name="root"),
    re_path(r"^(?P<subpath>.*)$", views.entry, name="proxy"),
]
