from rest_framework import permissions


class IsOwnerPermission(permissions.BasePermission):
    """
    Check if the request user is the owner of the object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the request user is the owner of the object.
        SAFE_METHODS are methods that are considered safe, such as GET, HEAD, and OPTIONS.
        """
        if request.method == permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    The request is user an admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        """
        Check if the request user is an admin or the request is a read-only request.
        SAFE_METHODS are methods that are considered safe, such as GET, HEAD, and OPTIONS.
        """
        if request.method in permissions.SAFE_METHODS:
            return True