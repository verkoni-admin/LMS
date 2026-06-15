from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView, TokenRefreshView

from accounts.views import register_user

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", TokenObtainPairView.as_view(), name="obtain_access_token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh_token"),
    path("logout/", TokenBlacklistView.as_view(), name="blacklist_token"),
]


