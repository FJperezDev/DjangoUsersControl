from rest_framework import permissions

class RolePermission(permissions.BasePermission):
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and (
            user.role in self.allowed_roles or user.is_superuser
        )