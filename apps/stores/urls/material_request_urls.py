from django.urls import path
from ..views import material_request_views

app_name = "material_requests"

urlpatterns = [
    path("", material_request_views.ListMaterialRequests.as_view(), name="index"),
    path(
        "create/", material_request_views.CreateMaterialRequest.as_view(), name="create"
    ),
    path(
        "update/<int:pk>",
        material_request_views.UpdateMaterialRequest.as_view(),
        name="update",
    ),
    path(
        "delete/<int:pk>",
        material_request_views.DeleteMaterialRequest.as_view(),
        name="delete",
    ),
]
