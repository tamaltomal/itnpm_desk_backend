from django.urls import path
from . import views

urlpatterns = [
    path('task/<uuid:id>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('task/create/', views.TaskCreateView.as_view(), name='task_create'),
    path('task/update/<uuid:id>/', views.TaskUpdateView.as_view(), name='task_update'),
    path('task/delete/<uuid:id>/', views.TaskDeleteAPIView.as_view(), name='task_delete'),
    path('tasks/', views.TaskListView.as_view(), name='task_list'),
]