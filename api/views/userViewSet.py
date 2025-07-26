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
            'find_by_email': {'superadmin', 'admin'},
            'find_by_username': {'superadmin', 'admin'},
            'find_by_username_or_email': {'superadmin', 'admin'},
        'destroy_by_username_or_email': {'superadmin'},
        }

        roles = action_roles.get(self.action, None)
        if isinstance(roles, set):
            return [RolePermission(roles)]
        else:
            return [permissions.IsAuthenticated()]
    
    @action(detail=False, methods=['get'], url_name="find-by", url_path="find")
    def find_by_username_or_email(self, request, email=None, username=None):
        if not (email or username):
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = self.queryset.get(username=username) if username else self.queryset.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


    