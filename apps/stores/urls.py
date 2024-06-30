from django.urls import path, include
from . import views

app_name = "stores"

store_urls = [
    # Stores
    path("", views.ListStores.as_view(), name="index_store"),
    path("create/", views.CreateStore.as_view(), name="create_store"),
    path("update/<int:pk>", views.UpdateStore.as_view(), name="update_store"),
    path("delete/<int:pk>", views.DeleteStore.as_view(), name="delete_store"),
    # Stocks
    path("<int:pk_store>/stocks/", include("apps.stores.stock_urls")),
]

item_urls = [
    # Items
    path("items/", views.ListItems.as_view(), name="index_item"),
    path("items/create/", views.CreateItem.as_view(), name="create_item"),
    path("items/update/<int:pk>", views.UpdateItem.as_view(), name="update_item"),
    path("items/delete/<int:pk>", views.DeleteItem.as_view(), name="delete_item"),
]

item_request_urls = [
    # Item Requests
    path("item_requests/", views.ListItemRequests.as_view(), name="index_item_request"),
    path(
        "item_requests/create/",
        views.CreateItemRequest.as_view(),
        name="create_item_request",
    ),
    path(
        "item_requests/update/<int:pk>",
        views.UpdateItemRequest.as_view(),
        name="update_item_request",
    ),
    path(
        "item_requests/delete/<int:pk>",
        views.DeleteItemRequest.as_view(),
        name="delete_item_request",
    ),
]

item_requirement_urls = [
    # Item Requirements
    path(
        "item_requirements/",
        views.ListItemRequirements.as_view(),
        name="index_item_requirement",
    ),
    path(
        "item_requirements/create/",
        views.CreateItemRequirement.as_view(),
        name="create_item_requirement",
    ),
    path(
        "item_requirements/update/<int:pk>",
        views.UpdateItemRequirement.as_view(),
        name="update_item_requirement",
    ),
    path(
        "item_requirements/delete/<int:pk>",
        views.DeleteItemRequirement.as_view(),
        name="delete_item_requirement",
    ),
    # Helpers
]

material_request_urls = [
    # Material Requests
    path(
        "material_requests/",
        views.ListMaterialRequests.as_view(),
        name="index_material_request",
    ),
    path(
        "material_requests/create/",
        views.CreateMaterialRequest.as_view(),
        name="create_material_request",
    ),
    path(
        "material_requests/update/<int:pk>",
        views.UpdateMaterialRequest.as_view(),
        name="update_material_request",
    ),
    path(
        "material_requests/delete/<int:pk>",
        views.DeleteMaterialRequest.as_view(),
        name="delete_material_request",
    ),
]


material_requirement_urls = [
    # Material Requirements
    path(
        "material_requirements/",
        views.ListMaterialRequirements.as_view(),
        name="index_material_requirement",
    ),
    path(
        "material_requirements/create/",
        views.CreateMaterialRequirement.as_view(),
        name="create_material_requirement",
    ),
    path(
        "material_requirements/update/<int:pk>",
        views.UpdateMaterialRequirement.as_view(),
        name="update_material_requirement",
    ),
    path(
        "material_requirements/delete/<int:pk>",
        views.DeleteMaterialRequirement.as_view(),
        name="delete_material_requirement",
    ),
]

urlpatterns = (
    store_urls
    + item_urls
    + item_request_urls
    + item_requirement_urls
    + material_requirement_urls
    + material_request_urls
)
