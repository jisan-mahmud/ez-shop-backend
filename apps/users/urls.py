# apps/users/urls.py
from django.urls import path
from .views import (
    RegisterView, LoginView,
    ProfileView, ChangePasswordView,
    AdminUserListView, AdminMerchantListView, AdminDeactivateUserView,
)

urlpatterns = [
    # auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),

    # profile
    path("profile/", ProfileView.as_view(), name="profile"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),

    # admin only
    path("admin/users/", AdminUserListView.as_view(), name="admin-users"),
    path("admin/merchants/", AdminMerchantListView.as_view(), name="admin-merchants"),
    path("admin/users/<int:user_id>/deactivate/", AdminDeactivateUserView.as_view(), name="admin-deactivate"),
]