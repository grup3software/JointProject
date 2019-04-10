from django.urls import path
from django.conf.urls import url
from django.utils import timezone
from django.views.generic import DetailView, ListView
from .models import *
from .views import *

app_name = "storageandgo"

urlpatterns = [
    # LIST OF TASKS
    path('tasks',
         ListUnasignedTasks.as_view(),
         name='unasigned_task_list'),

    path('tasks/<int:pk>/assign',
         TaskUpdate.as_view(),
         name='assign_task'),

    url(r'^gestor_home/', gestor_home, name="gestor_home"),
    url(r'^gestor_arealizar', gestor_arealizar, name="gestor_arealizar"),
    url(r'^gestor_realizando', gestor_realizando, name="gestor_realizando"),
    url(r'^gestor_finalizado', gestor_finalizado, name="gestor_finalizado"),
    url(r'^gestor_añadirtarea', gestor_añadirtarea, name="gestor_añadirtarea"),
]
