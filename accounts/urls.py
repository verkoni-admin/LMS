from django.urls import path
from rest_framework_simplejwt.views import TokenBlacklistView

from .views import auth_views, profile_views

urlpatterns = [
    path("register/", auth_views.register_user, name="register"),
    path("login/", auth_views.login_user, name="obtain_access_token"),
    path("refresh/", auth_views.refresh_jwt_token, name="refresh_token"),
    path("logout/", TokenBlacklistView.as_view(), name="blacklist_token"),
    path("instructor-profile/", profile_views.update_instructor_profile, name="instructor_profile"),
    path("user-profile/", profile_views.base_profile, name="user_profile"),
]


