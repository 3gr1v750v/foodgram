from rest_framework import permissions
from rest_framework.exceptions import MethodNotAllowed


class AuthorOrReadOnly(permissions.BasePermission):
    """Определение логики разрешения доступа к объекту на основе авторства."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
        )

class DjoserEndpointsLockResponse(permissions.BasePermission):
    """Определение логики разрешения доступа к отдельным эндпоинтам Djoser."""
    def has_permission(self, request, view):
        raise MethodNotAllowed(
            request.method,
            detail="Обращение к эндпоинту с данным методом не разрешено.")
