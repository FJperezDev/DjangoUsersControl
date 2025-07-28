from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

class LoggedUserView(APIView):  
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        return Response({
            "username": request.user.username,
            "email": request.user.email,
            "role": request.user.role,
            "is_superuser": request.user.is_superuser
        }, 
        status=status.HTTP_200_OK)
    
