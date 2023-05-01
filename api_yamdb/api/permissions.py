"""
Разрешения приложения api.

IsAdmin                                -- Доступ только для админа.
IsAuthorOrIsModeratorOrAdminOrReadOnly -- Общие ограничения на просмотр
                                          для всех видов пользователей.
IsAdminOrReadOnly                      -- Права изменения у админа,
                                          остальным только просмотр.
"""

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS


class IsAdmin(permissions.BasePermission):
    """
    Доступ только для админа.

    has_permission -- Проверяет общий доступ.
    """

    def has_permission(self, request, view):
        """Проверяет общий доступ."""
        return (request.user.is_authenticated
                and (request.user.is_admin or request.user.is_superuser))


class IsAuthorOrIsModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Общие ограничения на просмотр для всех видов пользователей.

    has_permission        -- Проверяет общий доступ.
    has_object_permission -- Проверяет доступ к объекту.
    """

    def has_permission(self, request, view):
        """Проверяет общий доступ."""
        return (request.method in SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        """Проверяет доступ к объекту."""
        return (request.method in SAFE_METHODS
                or request.user == obj.author
                or request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Права изменения у админа, остальным только просмотр.

    has_permission -- Проверяет общий доступ.
    """

    def has_permission(self, request, view):
        """Проверяет общий доступ."""
        return (
            request.method in SAFE_METHODS
            or (request.user.is_authenticated
                and (request.user.is_superuser or request.user.is_admin))
        )
