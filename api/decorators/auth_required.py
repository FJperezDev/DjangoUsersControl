from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def auth_required():
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            user = request.user
            if not user or not user.is_authenticated:
                return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator
