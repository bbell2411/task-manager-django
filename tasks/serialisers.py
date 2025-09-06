from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Task

class TaskSerialiser(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    
    class Meta:
        model= Task
        fields=["title","description","completed","user","created_at","updated_at"]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']