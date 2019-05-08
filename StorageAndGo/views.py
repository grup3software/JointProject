# FOR LOADING API
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import ListView, UpdateView, CreateView

from .forms import *


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


class ListRealizing(ListView):
    template_name = 'gestor-sala-realizando.html'

    def get_context_data(self, **kwargs):
        context = super(ListRealizing, self).get_context_data(**kwargs)
        operator = TaskOperator.objects.filter(accepted=True, finished=False)
        maintenance = TaskMaintenance.objects.filter(accepted=True, finished=False)
        context['task_operator'] = operator
        context['task_maintenance'] = maintenance
        return context

    def get_queryset(self):
        queryset = Task.objects.filter()

        return queryset


class ListFinalized(ListView):
    template_name = 'gestor-sala-finalizado.html'

    def get_context_data(self, **kwargs):
        context = super(ListFinalized, self).get_context_data(**kwargs)
        operator = TaskOperator.objects.filter(finished=True)
        maintenance = TaskMaintenance.objects.filter(finished=True)
        context['task_operator'] = operator
        context['task_maintenance'] = maintenance
        return context

    def get_queryset(self):
        queryset = Task.objects.filter()

        return queryset


class AvariaList(ListView):
    template_name = 'avaria_list.html'

    def get_context_data(self, **kwargs):
        context = super(AvariaList, self).get_context_data(**kwargs)
        avaria = Avaria.objects.filter(accepted=False)
        context['task_avaria'] = avaria
        return context

    def get_queryset(self):
        queryset = Avaria.objects.filter()

        return queryset


class TaskUpdate(UpdateView):
    model = Task
    fields = ['user']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskUpdate, self).form_valid(form)


# class TaskUpdate(UpdateView):
#     model = Task
#     fields = ['user']
#     template_name = "form.html"
#
#     def form_valid(self, form):
#         form.instance.sender = self.request.user
#         return super(TaskUpdate, self).form_valid(form)


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


def mapa_salas(request):
    # getting our template
    template = loader.get_template('mapa-salas.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())


class TaskAccept(UpdateView):
    model = Task
    fields = ['accepted']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskAccept, self).form_valid(form)


class TaskOperatorModify(UpdateView):
    model = TaskOperator
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskOperatorModify, self).form_valid(form)


class TaskMaintenanceModify(UpdateView):
    model = TaskMaintenance
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        # return super(TaskMaintenanceModify, self).form_valid(form)
        url_report = self.request.META.get('HTTP_REFERER')
        return redirect(url_report)


class TaskAvariaModify(UpdateView):
    model = Avaria
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskAvariaModify, self).form_valid(form)


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


def CreateSalaView(request):
    if request.method == 'POST':
        form = CreateSala(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('storageandgo:mapa_salas')
    else:
        form = CreateSala()
        return render(request, "form.html", {'form': form})


def createTask(contenidor):

    print(contenidor)

    rooms = Room.objects.all()

    avaliableRoom = 0

    for room in rooms:
        if room.temperature > contenidor.tempMinDegree and room.temperature < contenidor.tempMaxDegree and room.capacity-room.contenidorsInside > contenidor.qty:
                avaliableRoom = room
                break

    if avaliableRoom == 0:
        print(contenidor)
        task = TaskOperator(description="No hi ha sales disponibles per a conteidors de " + contenidor["name"], product=contenidor["name"], quantity=contenidor["qty"])
        task.save()
    else:
        task = TaskOperator(description="Moure " + contenidor.qty + "conteidors de " + contenidor.name, product=contenidor.name, origin="Moll descarrega", destination=avaliableRoom.description, quantity=contenidor.qty)
        task.save()


class ManifestoCreate(CreateView):
    model = Manifesto
    fields = ['ref']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        ref = form.cleaned_data['ref']

        data = requests.get('https://ourfarms.herokuapp.com/apiRest/REF/?ref=' + ref,
                            auth=('GR3', 'gr3124567890')).json()

        contenidors = []
        for contenidor in data[0]['Products']:
            cont = Contenidor(**contenidor)
            cont.save()
            contenidors.append(cont)
            createTask(contenidor);


        del data[0]['Products']

        man = Manifesto(**data[0])
        man.save()
        for contenidor in contenidors:
            man.Products.add(contenidor)

        return redirect(reverse('storageandgo:gestor_arealizar'))


def tecnics_home(request):
    # getting our template
    template = loader.get_template('tecnics-home.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())


def tecnics_arealitzar(request):
    # getting our template
    template = loader.get_template('tecnics-a-realizar.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())


def operari_home(request):
    # getting our template
    template = loader.get_template('operari-home.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

def añadir_sala(request):
    # getting our template
    template = loader.get_template('añadir_sala_form.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())
