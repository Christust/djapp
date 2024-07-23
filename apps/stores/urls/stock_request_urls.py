from rest_framework.routers import DefaultRouter
from ..views.stock_request_views import StockRequestViewSet

router = DefaultRouter()

router.register(r"", StockRequestViewSet)

urlpatterns = [] + router.urls
