from rest_framework import permissions


class IsSuperuserPermission(permissions.BasePermission):
    """Доступ только для superuser"""

    def has_permission(self, request, view):
        return request.user.is_superuser
