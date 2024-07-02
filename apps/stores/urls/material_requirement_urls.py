from django.urls import path
from .. import app_views

app_name = "material_requirements"

urlpatterns = [
    path("", app_views.ListMaterialRequirements.as_view(), name="index"),
    path("create/", app_views.CreateMaterialRequirement.as_view(), name="create"),
    path(
        "update/<int:pk>", app_views.UpdateMaterialRequirement.as_view(), name="update"
    ),
    path(
        "delete/<int:pk>", app_views.DeleteMaterialRequirement.as_view(), name="delete"
    ),
]
