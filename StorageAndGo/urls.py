from django.urls import path
from django.conf.urls import url
from django.utils import timezone
from django.views.generic import DetailView, ListView
from .models import *
from .views import *

app_name = "storageandgo"

urlpatterns = [

    # LIST OF TASKS

    # path('gestor_creacion_tarea/', CreateTaskView, name="CreateTaskView"),
    # url(r'^gestor_home/', gestor_home, name="gestor_home"),
    # url(r'^gestor_arealizar', gestor_arealizar, name="gestor_arealizar"),


    #                                             GESTOR SALA


    path('gestor_home/', ListTasks.as_view(), name='task_list'),
    path('gestor_arealizar/', ListTasks.as_view(), name="gestor_arealizar"),
    url(r'^gestor_realizando/', ListRealizing.as_view(), name="gestor_realizando"),
    url(r'^gestor_finalizado/', ListFinalized.as_view(), name="gestor_finalizado"),
    path('gestor_creacion_tarea/', CreateTaskView, name="CreateTaskView"),

    path('pedido/', ManifestoCreate.as_view(), name="CreateManifesto"),

    path('afegir_sala/', CreateSalaView, name="afegir_sala"),


    #                                              SALA


    url(r'^mapa_salas/', mapa_salas, name="mapa_salas"),

    #                                              OPERARI


    path('operari_home/', operari_home, name="operari_home"),
    url(r'^operari_arealizar/', operari_arealitzar, name="operari_arealitzar"),
    url(r'^operari_realizando/', operari_realizando, name="operari_realizando"),
    url(r'^operari_finalizado/', operari_finalizado, name="operari_finalizado"),

    #                                              TECNIC


    url(r'^tecnics_home/', tecnics_home, name="tecnics_home"),
    url(r'^tecnics_arealizar/', tecnics_arealitzar, name="tecnics_arealizar"),
    url(r'^tecnics_realitzant/', tecnics_realizando, name="tecnics_realizando"),
    url(r'^tecnics_finalizado/', tecnics_finalizado, name="tecnics_finalizado"),

    path('avaria_list/', AvariaList.as_view(), name="AvariaList"),


    #                                              TASKS


    path('unasigned_tasks/',
         ListUnasignedTasks.as_view(),
         name='unasigned_task_list'),

    path('tasks/<int:pk>/assign/',
         TaskUpdate.as_view(),
         name='assign_task'),
    path('tasks/<int:pk>/accept/',
         task_accept,
         name='accept_task'),

    path('tasks/<int:pk>/finish/',
         task_finish,
         name='finish_task'),

    path('tasks/<int:pk>/modify_operator/',
         TaskOperatorModify.as_view(),
         name='modify_operator'),

    path('tasks/<int:pk>/modify_maintenance/',
         TaskMaintenanceModify.as_view(),
         name='modify_maintenance'),

    path('tasks/<int:pk>/modify_avaria/',
         TaskAvariaModify.as_view(),
         name='modify_avaria'),

    #                                               CEO

    path('afegir_sala/', CreateSalaView, name="afegir_sala"),
    # path('gestor_creacion_tarea/', CreateTaskView, name="CreateTaskView"),
]
