from django.urls import path
from .. import app_views

app_name = "material_requests"

urlpatterns = [
    path("", app_views.ListMaterialRequests.as_view(), name="index"),
    path("create/", app_views.CreateMaterialRequest.as_view(), name="create"),
    path("update/<int:pk>", app_views.UpdateMaterialRequest.as_view(), name="update"),
    path("delete/<int:pk>", app_views.DeleteMaterialRequest.as_view(), name="delete"),
]
