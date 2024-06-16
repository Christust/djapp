from django.urls import path
from apps.users import views
from django.contrib.auth.decorators import login_required

app_name = "users"

urlpatterns = [
    path("", login_required(views.index), name="index")
]
