from django.shortcuts import render
from rest_framework import generics
from .serializers import TaskListSerializer, TaskDetailSerializer
from .models import Task

# Create your views here.
class TaskListView(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskListSerializer

class TaskDetailView(generics.RetrieveAPIView):
    lookup_field = 'id'
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

class TaskUpdateView(generics.RetrieveUpdateAPIView):
    lookup_field = 'id'
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer

class TaskDeleteAPIView(generics.DestroyAPIView):
    lookup_field = 'id'
    queryset = Task.objects.all()