from django.conf.urls import url
from django.urls import path

from .views import *


app_name = "storageandgo"

urlpatterns = [

    path('', redirect_to_home),

    # url(r'login_success/$', views.login_success, name='login_success'),
    # url(r'log_out_success/$', views.logout_view, name='logout_success'),

    # LIST OF TASKS

    path('avaria_list/', AvariaList.as_view(), name="AvariaList"),


    #GESTOR SALA

    path('gestor_home/', ListTasks.as_view(), name='task_list'),
    path('gestor_historial', ListHistoryTasks.as_view(), name='task_history_list'),
    path('gestor_arealizar/', ListTasks.as_view(), name="gestor_arealizar"),
    path('gestor_realizando/', ListRealizing.as_view(), name="gestor_realizando"),
    path('gestor_finalizado/', ListFinalized.as_view(), name="gestor_finalizado"),
    path('gestor_creacion_tarea_operario/', CreateOperatorTaskView, name="CreateOperatorTaskView"),
    path('gestor_creacion_tarea_tecnic/', CreateTecnicTaskView, name="CreateTecnicTaskView"),
    path('pedido/', ManifestoCreate.as_view(), name="CreateManifesto"),


    #SALA

    path('mapa_salas/', mapa_salas, name="mapa_salas"),

    path('afegir_sala/', CreateSalaView, name="afegir_sala"),
    path('sala/<int:pk>/', sala_detail, name='sala_detail'),
    path('sala/<int:pk>/delete', sala_delete, name='sala_delete'),
    path('sala/<int:pk>/modify/',
         SalaModify.as_view(),
         name='modify_sala'),


    #OPERARI

    # path('operari_home/', operari_home, name="operari_home"),
    path('operari_home/', operari_arealitzar, name="operari_home"),
    path('operari_arealizar/', operari_arealitzar, name="operari_arealitzar"),
    path('operari_realizando/', operari_realizando, name="operari_realizando"),
    path('operari_finalizado/', operari_finalizado, name="operari_finalizado"),
    path('operari_notification/', operari_notification, name="operari_notification"),
    path('operari_detall_tasca/<pk>/', operari_detall_tasca, name="operari_detall_tasca"),

    #TECNIC

    # path('tecnics_home/', tecnics_home, name="tecnics_home"),
    path('tecnics_home/', tecnics_arealitzar, name="tecnics_home"),
    path('tecnics_arealizar/', tecnics_arealitzar, name="tecnics_arealizar"),
    path('tecnics_realitzant/', tecnics_realizando, name="tecnics_realizando"),
    path('tecnics_finalizado/', tecnics_finalizado, name="tecnics_finalizado"),
    path('create_averia/', CreateAvariaView, name = "afegir_averia"),
    path('tecnics_detall_tasca/<pk>/', tecnics_detall_tasca, name="tecnics_detall_tasca"),


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
    path(r'informes/', InformeSla.as_view(), name="informe"),
    path('complets_sla/', complets_sla, name="complets_sla"),
    path('capacitat/', capacitat, name="capacitat"),
    path('complets_mes/', complets_mes, name="complets_mes"),
    path('ceo_historial', ListHistoryTasks.as_view(), name='task_history_list'),
    path('ceo_detall_avaria/<pk>/', ceo_detall_averia, name="ceo_detall_avaria"),
]
