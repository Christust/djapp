from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ..views.store_views import StoreViewSet

router = DefaultRouter()

router.register(r"", StoreViewSet)

urlpatterns = [] + router.urls
