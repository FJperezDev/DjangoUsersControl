from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import authenticate, login
from ..models import CustomUser
from ..serializers import CustomUserSerializer

class LoginView(APIView):  

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        user = authenticate(request, username=email, password=password)


        if not user:
            return Response({'error': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        login(request, user)  # Log the user in
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': CustomUserSerializer(user).data
        })
