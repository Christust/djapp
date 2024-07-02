from django.urls import path
from .. import app_views

app_name = "stocks"

urlpatterns = [
    # Stocks
    path("", app_views.ListStocks.as_view(), name="index"),
    path("create/", app_views.CreateStock.as_view(), name="create"),
    path("update/<int:pk>", app_views.UpdateStock.as_view(), name="update"),
    path("delete/<int:pk>", app_views.DeleteStock.as_view(), name="delete"),
]
