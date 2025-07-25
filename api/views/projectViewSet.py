from django.shortcuts import render
from ..models import CustomUser
from ..serializers import CustomUserSerializer
from rest_framework import viewsets, permissions

# Create your views here.

class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]