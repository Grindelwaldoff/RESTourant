from django.contrib.auth import get_user_model
from rest_framework.permissions import BasePermission, SAFE_METHODS


User = get_user_model()


class IsBusiness(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (request.user.is_superuser
            or request.user.is_business)
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.business == request.user
            or request.user.is_superuser
            or request.method in SAFE_METHODS
        )