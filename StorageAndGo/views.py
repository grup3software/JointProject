from django.shortcuts import render
from .models import *
from django.views.generic import ListView, UpdateView
from django.template import loader
from django.http import HttpResponse

# Create your views here.


class ListUnasignedTasks(ListView):
    template_name = 'unasigned_task_list.html'

    # Modifying the get_context_data method

    def get_context_data(self, **kwargs):
        context = super(ListUnasignedTasks, self).get_context_data(**kwargs)
        operator = TaskOperator.objects.filter(user=None)
        maintenance = TaskMaintenance.objects.filter(user=None)
        context['unasigned_operator'] = operator
        context['unasigned_maintenance'] = maintenance
        return context

    def get_queryset(self):
        queryset = Task.objects.filter(user=None)

        return queryset


class TaskUpdate(UpdateView):
    model = Task
    fields = ['user']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskUpdate, self).form_valid(form)

def gestor_home(request):
    # getting our template
    template = loader.get_template('gestor-sala-home.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

def gestor_arealizar(request):
    # getting our template
    template = loader.get_template('gestor-sala-a-realizar.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

def gestor_realizando(request):
    # getting our template
    template = loader.get_template('gestor-sala-realizando.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

def gestor_finalizado(request):
    # getting our template
    template = loader.get_template('gestor-sala-finalizado.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

def gestor_añadirtarea(request):
    # getting our template
    template = loader.get_template('gestor-sala-añadir-tarea.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())
