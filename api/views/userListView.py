
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from api.serializers import CustomUserSerializer
from api.decorators.role_required import role_required

User = get_user_model()

class UserListView(APIView):
    @role_required('superteacher')
    def get(self, request):
        users = User.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)