from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__' # equiv to ('id', 'name', 'description', 'technology', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')
        