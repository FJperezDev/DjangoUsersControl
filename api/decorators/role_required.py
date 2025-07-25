from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def role_required(required_role):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.role == required_role or user.is_superuser:
                return view_func(self, request, *args, **kwargs)
            return Response({'error': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        return _wrapped_view
    return decorator