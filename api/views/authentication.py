from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password

from ..serializers import CustomUserSerializer
from ..models import CustomUser
from ..permissions import IsNotAuthenticated   

class LoggedUserView(APIView):  
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(CustomUserSerializer(request.user).data, status=status.HTTP_200_OK)
    
class LoginView(APIView):  
    permission_classes = [IsNotAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request, username=email, password=password)

        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user) 

        return Response({'message': 'Login Succesful', 'user': CustomUserSerializer(user).data})

class LogoutView(APIView):  
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "User is not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


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
