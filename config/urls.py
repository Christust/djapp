from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
from apps.users.views import Login, Logout

urlpatterns = [
    # Auth
    path("login/", Login.as_view(), name="login"),
    path("logout/", Logout.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # Routers
    path("users/", include("apps.users.urls")),
    path("branches/", include("apps.branches.urls")),
    path("stores/", include("apps.stores.urls.store_urls")),
    path("items/", include("apps.stores.urls.item_urls")),
    path("stocks/", include("apps.stores.urls.stock_urls")),
    path("material_requests/", include("apps.stores.urls.material_request_urls")),
    path("item_requests/", include("apps.stores.urls.item_request_urls")),
]
