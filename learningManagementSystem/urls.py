from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView, TokenBlacklistView
from . import views


urlpatterns = [
    path("get-user/", views.get_user, name="get_user"),
]

