from django.urls import path
from django.conf.urls import url
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

    path('tasks/<int:pk>/assign/',
         TaskUpdate.as_view(),
         name='assign_task'),

    # url(r'^gestor_home/', gestor_home, name="gestor_home"),
    path('gestor_home/', ListTasks.as_view(), name='task_list'),
    # url(r'^gestor_arealizar', gestor_arealizar, name="gestor_arealizar"),
    path('gestor_arealizar/', ListTasks.as_view(), name="gestor_arealizar"),
    url(r'^gestor_realizando/', gestor_realizando, name="gestor_realizando"),
    url(r'^gestor_finalizado/', gestor_finalizado, name="gestor_finalizado"),
    url(r'^mapa_salas/', mapa_salas, name="mapa_salas"),

    path('avaria_list/', AvariaList.as_view(), name="AvariaList"),
    path('pedido/', ManifestoCreate.as_view(), name="CreateManifesto"),

    path('gestor_creacion_tarea/', CreateTaskView, name="CreateTaskView"),

    path('tasks/<int:pk>/accept/',
         TaskAccept.as_view(),
         name='accept_task'),

    path('tasks/<int:pk>/modify_operator/',
         TaskOperatorModify.as_view(),
         name='modify_operator'),

    path('tasks/<int:pk>/modify_maintenance/',
         TaskMaintenanceModify.as_view(),
         name='modify_maintenance'),

    path('tasks/<int:pk>/modify_avaria/',
         TaskAvariaModify.as_view(),
         name='modify_avaria'),

    path('operari_home/', operari_home, name="operari_home"),
]
