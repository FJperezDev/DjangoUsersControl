from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from ..models import CustomUser
from ..serializers import CustomUserSerializer
from ..decorators import role_required, auth_required

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
    permission_classes = [permissions.AllowAny]

    @role_required({'superteacher', 'teacher'})
    def list(self, request):
        users = self.queryset
        serializer = self.serializer_class(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @auth_required()
    def retrieve(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @role_required('superteacher')
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @role_required('superteacher')
    def update(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @role_required('superteacher')
    def destroy(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)