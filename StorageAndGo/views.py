from django.shortcuts import render, redirect
from .models import *
from django.views.generic import ListView, UpdateView
from django.template import loader
from django.http import HttpResponse
from .forms import *
from django.views.generic.edit import FormView

# Create your views here.

class ListUnasignedTasks(ListView):
    template_name = 'unasigned_task_list.html'

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


class ListTasks(ListView):
    template_name = 'task_list.html'

    def get_context_data(self, **kwargs):
        context = super(ListTasks, self).get_context_data(**kwargs)
        operator = TaskOperator.objects.filter(accepted=False)
        maintenance = TaskMaintenance.objects.filter(accepted=False)
        context['task_operator'] = operator
        context['task_maintenance'] = maintenance
        return context

    def get_queryset(self):
        queryset = Task.objects.filter()

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


class TaskAccept(UpdateView):
    model = Task
    fields = ['accepted']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskAccept, self).form_valid(form)


class TaskModify(UpdateView):
    model = TaskOperator
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskModify, self).form_valid(form)


def CreateTaskView(request):
    if request.method == "POST":
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('storageandgo:gestor_arealizar')

    else:

        form = CreateTaskForm()

        return render(request, "form.html", {'form': form})


'''class CreateTaskView(FormView):
    template_name = 'form.html'
    form = CreateTaskForm()
    success_url = '/Task-Successfull/'

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        return super().form_valid(form)'''
