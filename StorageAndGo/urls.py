from django.urls import path
from django.utils import timezone
from django.views.generic import DetailView, ListView
from .models import *
from .views import *

app_name = "storageandgo"

urlpatterns = [
    # LIST OF TASKS
    path('unasigned_tasks/',
         ListUnasignedTasks.as_view(),
         name='unasigned_task_list'),

    path('tasks/',
         ListTasks.as_view(),
         name='task_list'),

    path('tasks/<int:pk>/assign',
         TaskUpdate.as_view(),
         name='assign_task'),

    path('tasks/<int:pk>/accept',
         TaskAccept.as_view(),
         name='accept_task'),

    path('tasks/<int:pk>/modify',
         TaskModify.as_view(),
         name='modify_task'),
]
