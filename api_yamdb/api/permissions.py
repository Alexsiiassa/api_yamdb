from rest_framework import permissions

from reviews.models import UserRole


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            is_admin = request.user.role == UserRole.ADMIN.value
            return is_admin or request.user.is_superuser


class IsAdminModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == UserRole.ADMIN.value
                or request.user.role == UserRole.MODERATOR.value
                or obj.author == request.user)


class IsAnon(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return not request.user.is_authenticated
