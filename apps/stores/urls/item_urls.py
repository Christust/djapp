from rest_framework.routers import DefaultRouter
from ..views.item_views import ItemViewSet

router = DefaultRouter()

router.register(r"", ItemViewSet)

urlpatterns = [] + router.urls
