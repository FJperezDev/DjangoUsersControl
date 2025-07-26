from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
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
        if roles == 'any':
            return [permissions.IsAuthenticated()]
        elif isinstance(roles, set):
            return [RolePermission(roles)]
        else:
            return [permissions.AllowAny()]
    
    
    def find_by_username_or_email(self, request, username=None, email=None):
        if not username and not email:
            return Response({'error': 'Username or email must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if username:
                user = self.queryset.get(username=username)
            elif email:
                user = self.queryset.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def destroy_by_username_or_email(self, request, username=None, email=None):
        if not username and not email:
            return Response({'error': 'Username or email must be provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if username:
                user = self.queryset.get(username=username)
            elif email:
                user = self.queryset.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
