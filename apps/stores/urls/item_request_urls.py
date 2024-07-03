from rest_framework.routers import DefaultRouter
from ..views.item_request_views import ItemRequestViewSet

router = DefaultRouter()

router.register(r"", ItemRequestViewSet)

urlpatterns = [] + router.urls
