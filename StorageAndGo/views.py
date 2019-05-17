# FOR LOADING API
import ctypes

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.views.generic import ListView, UpdateView, CreateView

from .forms import *


# Create your views here.

#                                                    Index

# GESTOR SALA

# SALA

# OPERARI

# TECNIC

# TASKS

# CEO

# class TaskUpdate(UpdateView):
#     model = Task
#     fields = ['user']
#     template_name = "form.html"
#
#     def form_valid(self, form):
#         form.instance.sender = self.request.user
#         return super(TaskUpdate, self).form_valid(form)

@login_required(login_url='/accounts/login')
def redirect_to_home(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")

    group = User.objects.get(username=request.user).groups.all()[0]

    if group.name == "Ceo":
        return None
    elif group.name == 'Tecnic':
        return redirect("storageandgo:tecnics_home")
    elif group.name == 'Gestor':
        return redirect("storageandgo:task_list")

@login_required(login_url='/accounts/login')
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
            # createTask(contenidor)

        del data[0]['Products']

        man = Manifesto(**data[0])
        man.save()
        for contenidor in contenidors:
            man.products.add(contenidor)

        return redirect(reverse('storageandgo:gestor_arealizar'))


############################################ GESTOR SALA ##############################################################

@login_required(login_url='/accounts/login')
def gestor_home(request):
    # getting our template
    template = loader.get_template('Gestor_Sala/gestor-sala-home.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())


def gestor_arealizar(request):
    # getting our template
    template = loader.get_template('Gestor_Sala/gestor-sala-a-realizar.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def gestor_realizando(request):
    # getting our template
    template = loader.get_template('Gestor_Sala/gestor-sala-realizando.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def gestor_finalizado(request):
    # getting our template
    template = loader.get_template('Gestor_Sala/gestor-sala-finalizado.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def gestor_añadirtarea(request):
    # getting our template
    template = loader.get_template('gestor-sala-añadir-tarea.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def mapa_salas(request):
    # getting our template
    template = loader.get_template('mapa-salas.html')
    rooms = Room.objects.all()

    # rendering the template in HttpResponse
    # return HttpResponse(template.render())
    return render(request, "mapa-salas.html", {'rooms': rooms})


################################################# SALA ###############################################################
@login_required(login_url='/accounts/login')
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

############################################## OPERARI #################################################################

def operari_home(request):
    # getting our template
    template = loader.get_template('Operaris/operari-home.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())
@login_required(login_url='/accounts/login')
def operari_arealitzar(request):
    # getting our template
    template = loader.get_template('Operaris/operari-a-realitzar.html')

    tasques_operari_a_realitzar = TaskOperator.objects.filter(accepted=False)
    context={'tasques_operari_a_realitzar': tasques_operari_a_realitzar}

    # rendering the template in HttpResponse
    return HttpResponse(template.render(context))

def operari_realizando(request):
    # getting our template
    template = loader.get_template('Operaris/operari-realizando.html')

    tasques_operari_realizando = TaskOperator.objects.filter(accepted=True, finished=False)
    context = {'tasques_operari_realizando': tasques_operari_realizando}

    # rendering the template in HttpResponse
    return HttpResponse(template.render(context))

def operari_finalizado(request):
    # getting our template
    template = loader.get_template('Operaris/operari-finalizado.html')

    tasques_operari_finalizado = TaskOperator.objects.filter(finished=True)
    context = {'tasques_operari_finalizado': tasques_operari_finalizado}

    # rendering the template in HttpResponse
    return HttpResponse(template.render(context))




############################################### TECNIC #################################################################
@login_required(login_url='/accounts/login')
def tecnics_home(request):
    # getting our template
    template = loader.get_template('Tecnics/tecnics-home.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())


@login_required(login_url='/accounts/login')
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

@login_required(login_url='/accounts/login')
def tecnics_arealitzar(request):
    # getting our template
    template = loader.get_template('Tecnics/tecnics-a-realizar.html')

    tasques_tecnics_a_realitzar = TaskMaintenance.objects.filter(accepted=False)
    context = {'tasques_tecnics_a_realitzar': tasques_tecnics_a_realitzar}

    # rendering the template in HttpResponse
    return HttpResponse(template.render(context))

@login_required(login_url='/accounts/login')
def tecnics_realizando(request):
    # getting our template
    template = loader.get_template('Tecnics/tecnics-realizando.html')

    tasques_tecnics_realizando = TaskMaintenance.objects.filter(accepted=True, finished=False)
    context = {'tasques_tecnics_realizando': tasques_tecnics_realizando}

    # rendering the template in HttpResponse
    return HttpResponse(template.render(context))

@login_required(login_url='/accounts/login')
def tecnics_finalizado(request):
    # getting our template
    template = loader.get_template('Tecnics/tecnics-finalitzades.html')

    tasques_tecnics_finalitzades = TaskMaintenance.objects.filter(finished=True)
    context = {'tasques_tecnics_finalitzades': tasques_tecnics_finalitzades}

    # rendering the template in HttpResponse
    return HttpResponse(template.render(context))


################################################# TASKS ################################################################
@login_required(login_url='/accounts/login')
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

@login_required(login_url='/accounts/login')
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

@login_required(login_url='/accounts/login')
class ListRealizing(ListView):
    template_name = 'Gestor_Sala/gestor-sala-realizando.html'

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

@login_required(login_url='/accounts/login')
class ListFinalized(ListView):
    template_name = 'Gestor_Sala/gestor-sala-finalizado.html'

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

@login_required(login_url='/accounts/login')
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

@login_required(login_url='/accounts/login')
def gestor_home(request):
    # getting our template
    template = loader.get_template('gestor-sala-home.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def gestor_arealizar(request):
    # getting our template
    template = loader.get_template('gestor-sala-a-realizar.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def gestor_realizando(request):
    # getting our template
    template = loader.get_template('gestor-sala-realizando.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def gestor_finalizado(request):
    # getting our template
    template = loader.get_template('gestor-sala-finalizado.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def gestor_añadirtarea(request):
    # getting our template
    template = loader.get_template('gestor-sala-añadir-tarea.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())
@login_required(login_url='/accounts/login')
def gestor_registrar_manifest(request):
    # getting our template
    template = loader.get_template('gestor_sala_registrar_manifest.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
def mapa_salas(request):
    # getting our template
    template = loader.get_template('mapa-salas.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())

@login_required(login_url='/accounts/login')
class TaskAccept(UpdateView):
    model = Task
    fields = ['accepted']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskAccept, self).form_valid(form)
        # return HttpResponseRedirect(self.request.path_info)


@login_required(login_url='/accounts/login')
def task_accept(request, pk):
    task = Task.objects.get(pk=pk)
    task.accepted = True
    task.user = User.objects.get(username=request.user.username)
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login')
def task_finish(request, pk):
    task = Task.objects.get(pk=pk)
    task.finished = True
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login')
class TaskOperatorModify(UpdateView):
    model = TaskOperator
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        # FALTA GUARDAR MODIFICACIONS
        return redirect('storageandgo:operari_home')


@login_required(login_url='/accounts/login')
class TaskMaintenanceModify(UpdateView):
    model = TaskMaintenance
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        # return super(TaskMaintenanceModify, self).form_valid(form)
        url_report = self.request.META.get('HTTP_REFERER')
        return redirect(url_report)


@login_required(login_url='/accounts/login')
class TaskAvariaModify(UpdateView):
    model = Avaria
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskAvariaModify, self).form_valid(form)


@login_required(login_url='/accounts/login')
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


@login_required(login_url='/accounts/login')
def createTask(contenidor):
    print(contenidor)

    rooms = Room.objects.all()

    avaliable_room = 0
    if rooms:
        for room in rooms:
            if room.temperatureMin > contenidor["tempMinDegree"] and room.temperatureMax < contenidor["tempMaxDegree"] and room.capacity-room.contenidorsInside > contenidor['qty']:
                avaliable_room = room
                break

        if avaliable_room == 0:
            TaskOperator(description="Moure " + "conteidors de " + contenidor["name"], product=contenidor["name"],
                         origin=Room.objects.all()[0], destination=Room.objects.all()[0], quantity=contenidor["qty"],
                         accepted=False, finished=False)
            print(contenidor)
            # ctypes.windll.user32.MessageBoxW(0, "No hi ha sales disponibles per a conteidors de " + contenidor["name"], "Error", 1)
        else:
            task = TaskOperator(description="Moure " + str(contenidor['qty']) + "conteidors de " + contenidor['name'], product=contenidor['name'], origin=Room.objects.all()[0], destination=Room.objects.all()[0], quantity=contenidor['qty'], accepted=False, finished=False)
            task.save()
    else:
        ctypes.windll.user32.MessageBoxW(0, "No hi ha sales disponibles", "Error", 1)

######################################################## CEO ###########################################################

