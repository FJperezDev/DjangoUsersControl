from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

from ..serializers import CustomUserSerializer
from ..models import CustomUser

class LoggedUserView(APIView):  
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(CustomUserSerializer(request.user).data, status=status.HTTP_200_OK)

class LogoutView(APIView):  
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAllView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        tokens = OutstandingToken.objects.filter(user=request.user)
        for token in tokens:
            try:
                BlacklistedToken.objects.get_or_create(token=token)
            except Exception as e:
                pass
        return Response({"message": "Successfully logged out from all devices."}, status=status.HTTP_200_OK)

class RegisterView(APIView):
    def post(self, request):

        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not email or not password or not username:
            return Response({'error': 'Email, username, and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if CustomUser.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = CustomUser(
            email=email,
            username=username,
            password=make_password(password)  # Hash the password before saving
        )
        user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
