from django.urls import path
from apps.branches import views

urlpatterns = [
    path("", views.Home, name="index"),
]
