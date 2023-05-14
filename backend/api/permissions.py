from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):
    """Определение логики разрешения доступа к объекту на основе авторства."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )
