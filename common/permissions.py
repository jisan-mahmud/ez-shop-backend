from rest_framework.permissions import BasePermission

class IsMerchant(BasePermission):
    message = "You must be a merchant."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_merchant
        )


class IsAdmin(BasePermission):
    message = "You must be an admin."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.is_super_admin
        )