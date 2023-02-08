from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class IsBusiness(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_admin
            or request.user.is_business
        )
