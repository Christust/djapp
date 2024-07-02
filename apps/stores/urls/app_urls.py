from django.urls import path, include
from ..views import store_views

app_name = "stores"

urlpatterns = [
    # Stores
    path("", store_views.ListStores.as_view(), name="index"),
    path("create/", store_views.CreateStore.as_view(), name="create"),
    path("update/<int:pk>", store_views.UpdateStore.as_view(), name="update"),
    path("delete/<int:pk>", store_views.DeleteStore.as_view(), name="delete"),
    path("<int:pk>/", store_views.DetailStore.as_view(), name="detail"),
    # Items
    path("items/", include("apps.stores.urls.item_urls")),
    # Stocks
    path("stocks/", include("apps.stores.urls.stock_urls")),
]
