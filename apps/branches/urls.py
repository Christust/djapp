from django.urls import path
from . import views

app_name = "branches"
urlpatterns = [
    path("", views.ListBranches.as_view(), name="index"),
    path("create/", views.CreateBranch.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateBranch.as_view(), name="update"),
    path("delete/<int:pk>", views.DeleteBranch.as_view(), name="delete"),
    # Helpers
    path("ajax/load_states/", views.load_states, name="ajax_load_states"),
    path("ajax/load_cities/", views.load_cities, name="ajax_load_cities"),
]
