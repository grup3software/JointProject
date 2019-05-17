from django.urls import path
from .views import *

app_name = "storageandgo"

urlpatterns = [

    path('', redirect_to_home),

    # LIST OF TASKS

    path('avaria_list/', AvariaList.as_view(), name="AvariaList"),


    #GESTOR SALA

    path('gestor_home/', ListTasks.as_view(), name='task_list'),
    path('gestor_arealizar/', ListTasks.as_view(), name="gestor_arealizar"),
    path('gestor_realizando/', ListRealizing.as_view(), name="gestor_realizando"),
    path('gestor_finalizado/', ListFinalized.as_view(), name="gestor_finalizado"),
    path('gestor_creacion_tarea/', CreateTaskView, name="CreateTaskView"),
    path('pedido/', ManifestoCreate.as_view(), name="CreateManifesto"),


    #SALA

    path('mapa_salas/', mapa_salas, name="mapa_salas"),


    #OPERARI

    path('operari_home/', operari_home, name="operari_home"),
    path('operari_arealizar/', operari_arealitzar, name="operari_arealitzar"),
    path('operari_realizando/', operari_realizando, name="operari_realizando"),
    path('operari_finalizado/', operari_finalizado, name="operari_finalizado"),


    #TECNIC

    path('tecnics_home/', tecnics_home, name="tecnics_home"),
    path('tecnics_arealizar/', tecnics_arealitzar, name="tecnics_arealizar"),
    path('tecnics_realitzant/', tecnics_realizando, name="tecnics_realizando"),
    path('tecnics_finalizado/', tecnics_finalizado, name="tecnics_finalizado"),


    #TASKS

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


    #CEO
    # path('gestor_creacion_tarea/', CreateTaskView, name="CreateTaskView"),
]
