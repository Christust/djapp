from django.urls import path
from apps.branches import views

app_name = "branches"

urlpatterns = [
    path("", views.Home, name="index"),
    path("create/", views.CreateBranch, name = "create"),
    path('ajax/load_states/', views.load_states, name='ajax_load_states'),
    path('ajax/load_cities/', views.load_cities, name='ajax_load_cities'),

]
