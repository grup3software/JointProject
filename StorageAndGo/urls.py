from django.urls import path
from django.utils import timezone
from django.views.generic import DetailView, ListView
from .models import *

app_name = "storageandgo"

urlpatterns = [
    # LIST OF TASKS
    path('',
         ListView.as_view(
            queryset=Task.objects.filter(user=""),
            context_object_name='unasigned_tasks',
            template_name='unasigned_task_list.html'),
         name='unasigned_task_list'),
]
