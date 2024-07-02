from django.urls import path
from ..views import item_views

app_name = "items"

urlpatterns = [
    # Stocks
    path("", item_views.ListItems.as_view(), name="index"),
    path("create/", item_views.CreateItem.as_view(), name="create"),
    path("update/<int:pk>", item_views.UpdateItem.as_view(), name="update"),
    path("delete/<int:pk>", item_views.DeleteItem.as_view(), name="delete"),
]
