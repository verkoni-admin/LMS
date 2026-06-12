from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView


urlpatterns = [
    path("auth/login", TokenObtainPairView.as_view(), name="obtain_access_token"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("auth/logout/", TokenBlacklistView.as_view(), name="blacklist_token")
]

