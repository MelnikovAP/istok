from django.urls import path
from . import views

app_name = "mechanics"

urlpatterns = [
    path("", views.index, name="index"),
]
