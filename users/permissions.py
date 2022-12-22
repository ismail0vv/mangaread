from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """check if owner """

    def has_object_permission(self, request, view, obj):
        if request.method == permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is user an admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
