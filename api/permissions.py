"""Проверка прав."""
from rest_framework import permissions


class IsAuthenticatedAndIsInSaveMethodsPermission(permissions.BasePermission):
    """Разрешения для действия с корзиной покупок."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Разрешения на уровне объекта."""
        return obj.user == request.user
