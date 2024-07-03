from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()

router.register(r"countries", views.CountryViewSet)
router.register(r"states", views.StateViewSet)
router.register(r"cities", views.CityViewSet)
router.register(r"", views.BranchViewSet)


urlpatterns = [] + router.urls
