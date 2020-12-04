""""Здесь мы добавляем ращрешения"""
from rest_framework.permissions import BasePermission


class CartPermission(BasePermission):
    """Добавляем разрешения"""
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_normal)

    def has_object_permission(self, request, view, obj):
        """Ращрешение на удаление какого либо опредленного обьекта"""
        return request.user.is_authenticated and (request.user.is_normal or request.user.is_staff)

class IsCartHolder(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and obj.author_id == request.user