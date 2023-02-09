from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class IsAdminOrSelf(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_admin
            or request.user.is_superuser
            or request.method in SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user == obj or request.user.is_admin
            or request.user.is_superuser
        )
