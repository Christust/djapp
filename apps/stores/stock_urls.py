from django.urls import path
from . import views

app_name = "stocks"

urlpatterns = [
    # Stocks
    path("", views.ListStocks.as_view(), name="index"),
    path("create/", views.CreateStock.as_view(), name="create"),
    path("update/<int:pk>", views.UpdateStock.as_view(), name="update"),
    path("delete/<int:pk>", views.DeleteStock.as_view(), name="delete"),
]
