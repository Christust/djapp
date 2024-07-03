from rest_framework.routers import DefaultRouter
from ..views.stock_views import StockViewSet

router = DefaultRouter()

router.register(r"", StockViewSet)

urlpatterns = [] + router.urls
