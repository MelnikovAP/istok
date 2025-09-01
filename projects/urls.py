from django.urls import path
from .views import stand_detail

urlpatterns = [
    path('<slug:slug>/', stand_detail, name='stand_detail'),
]