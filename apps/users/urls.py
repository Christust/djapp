from django.urls import path
from django.contrib.auth.views import logout_then_login
from . import views

app_name = "users"
urlpatterns = [
    path("", views.ListUsers.as_view(), name="index"),
    path("create/", views.CreateUser.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateUser.as_view(), name="update"),
    path("delete/<int:pk>", views.DeleteUser.as_view(), name="delete"),
    # Auth
    path("login/", views.Login.as_view(template_name="login.html"), name="login"),
    path("logout/", logout_then_login, name="logout"),
    path(
        "change_password/<int:pk>",
        views.UpdateUserPassword.as_view(),
        name="change_password",
    ),
]
