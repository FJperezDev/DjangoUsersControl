from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import CustomUser
from ..serializers import CustomUserSerializer
from ..permissions import RolePermission

# Create your views here.

"""
UserViewSet is a Django REST Framework ModelViewSet for managing CustomUser instances.
By default, ModelViewSet provides the following actions:
    - list: Retrieves a list of all user instances.
    - retrieve: Retrieves a single user instance by primary key.
    - create: Creates a new user instance.
    - update: Updates an existing user instance (full or partial update).
    - destroy: Deletes a user instance.
This class overrides these methods to add custom permission checks and error handling:
    - list: Only accessible to users with 'superteacher' or 'teacher' roles.
    - retrieve: Requires authentication.
    - create: Only accessible to users with 'superteacher' role.
    - update: Only accessible to users with 'superteacher' role.
    - destroy: Only accessible to users with 'superteacher' role.
"""
class UserViewSet(viewsets.ModelViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        action_roles = {
            'list': {'superadmin', 'admin'},
            'retrieve': 'any',
            'create': {'superadmin'},
            'update': {'superadmin'},
            'partial_update': {'superadmin'},
            'destroy': {'superadmin'},
        }

        roles = action_roles.get(self.action, None)
        if isinstance(roles, set):
            return [RolePermission(roles)]
        else:
            return [permissions.IsAuthenticated()]
    
    def get_queryset(self):
        queryset = CustomUser.objects.all()
        username = self.request.query_params.get('username', None)
        email = self.request.query_params.get('email', None)

        if username and email:
            queryset = queryset.filter(username__icontains=username, email__icontains=email)
        elif username and not email:
            queryset = queryset.filter(username__icontains=username)
        elif email and not username:
            queryset = queryset.filter(email__icontains=email)
        return queryset