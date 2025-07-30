from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken

class RolePermission(permissions.BasePermission):
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and (
            user.role in self.allowed_roles or user.is_superuser
        )
    
class IsNotAuthenticated(permissions.BasePermission):
    """
    Permite solo a usuarios no autenticados (anónimos).
    """

    def has_permission(self, request, view):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return True
        try:
            refresh = RefreshToken(refresh_token)
            return False
        except:
            return True
