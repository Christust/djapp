from django.urls import path
from ..views import stock_views

app_name = "stocks"

urlpatterns = [
    # Stocks
    path("", stock_views.ListStocks.as_view(), name="index"),
    path("create/", stock_views.CreateStock.as_view(), name="create"),
    path("update/<int:pk>", stock_views.UpdateStock.as_view(), name="update"),
    path("delete/<int:pk>", stock_views.DeleteStock.as_view(), name="delete"),
]
