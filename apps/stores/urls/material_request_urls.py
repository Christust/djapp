from rest_framework.routers import DefaultRouter
from ..views.material_request_views import MaterialRequestViewSet

router = DefaultRouter()

router.register(r"", MaterialRequestViewSet)

urlpatterns = [] + router.urls
