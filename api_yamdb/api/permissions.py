from rest_framework import permissions


class CreaterOrAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.admin or request.user.is_superuser
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj == request.user
            or request.user.admin
            or request.user.is_superuser
        )


class ReadOnlySafeMethods(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAuthenticatedAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.admin or request.user.is_superuser
        )


class AdminOrReadOnlySafeMethods(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_active
            and request.user.admin
            or request.user.is_superuser
            or request.method in permissions.SAFE_METHODS
        )


class AdminAuthorModeratorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.moderator
            or request.user.admin
            or request.user.is_superuser
        )


class AdminEditUserNot(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
            and request.user.moderator
            or request.user.admin
            or request.user.is_superuser
        )
