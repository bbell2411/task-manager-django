from django.shortcuts import render
from .models import Task
from .serialisers import TaskSerialiser
from rest_framework import viewsets
from rest_framework.permissions import(IsAuthenticated, AllowAny)


class TaskViewSet(viewsets.ModelViewSet):
    queryset=Task.objects.all()
    serializer_class=TaskSerialiser
    permission_classes=[AllowAny] 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Task.objects.filter(user=self.request.user)
        return Task.objects.none()
    
    #test
    #add err handling
    #auth/token/post login/signup
    