# FOR LOADING API
import ctypes

import requests
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.views.generic import ListView, UpdateView, CreateView

from .forms import *
import datetime
import pytz


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

def logout_view(request):
    logout(request)


@login_required()
def redirect_to_home(request):
    if not request.user.is_authenticated:
        return redirect("/accounts/login/")

    group = User.objects.get(username=request.user).groups.all()[0]

    if group.name == "Ceo":
        return redirect("storageandgo:informe")
    elif group.name == 'Tecnic':
        return redirect("storageandgo:tecnics_home")
    elif group.name == 'Gestor':
        return redirect("storageandgo:task_list")
    elif group.name == 'Operari':
        return redirect("storageandgo:operari_home")


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
        if data:
            for contenidor in data[0]['Products']:
                cont = Contenidor(**contenidor)
                cont.save()
                contenidors.append(cont)
                createTask(contenidor)

            del data[0]['Products']

            man = Manifesto(**data[0])
            man.save()
            for contenidor in contenidors:
                man.products.add(contenidor)

        return redirect(reverse('storageandgo:gestor_arealizar'))


############################################ GESTOR SALA ##############################################################

@login_required()
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


@login_required()
def gestor_realizando(request):
    # getting our template
    template = loader.get_template('Gestor_Sala/gestor-sala-realizando.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())


@login_required()
def gestor_finalizado(request):
    # getting our template
    template = loader.get_template('Gestor_Sala/gestor-sala-finalizado.html')

    # rendering the template in HttpResponse
    return HttpResponse(template.render())


@login_required()
def mapa_salas(request):
    rooms = Room.objects.all()
    colors ={}
    group = User.objects.get(username=request.user).groups.all()[0]
    i = 1
    for room in rooms:
        if room.contenidorsInside /room.capacity > 0.50:
            colors['color'] = "w3-yellow"
        if room.contenidorsInside /room.capacity > 0.75:
            colors['color'] = "w3-orange"
        if room.contenidorsInside /room.capacity < 0.50:
            colors['color'] = "w3-green"
        i = i +1
    # rendering the template in HttpResponse
    if group.name == "Ceo":
        return render(request, "mapa-salas2.html", {'rooms': rooms})
    return render(request, "mapa-salas.html", {'rooms': rooms})


################################################# SALA ###############################################################


@login_required()
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


class SalaModify(UpdateView):
    model = Room
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(SalaModify, self).form_valid(form)


############################################## OPERARI #################################################################


@login_required()
def operari_home(request):
    # getting our template
    template = loader.get_template('Operaris/operari-home.html')

    # rendering the template in HttpResponse
    # return HttpResponse(template.render())
    return render(request, "Operaris/operari-home.html", {})


@login_required()
def operari_arealitzar(request):
    template = loader.get_template('Operaris/operari-a-realitzar.html')

    tasques_operari_a_realitzar = TaskOperator.objects.filter(accepted=False)
    context = {'tasques_operari_a_realitzar': tasques_operari_a_realitzar}

    # return HttpResponse(template.render(context))
    return render(request, "Operaris/operari-a-realitzar.html", context=context)


@login_required()
def operari_realizando(request):
    template = loader.get_template('Operaris/operari-realizando.html')

    tasques_operari_realizando = TaskOperator.objects.filter(accepted=True, finished=False, user=request.user)
    context = {'tasques_operari_realizando': tasques_operari_realizando}

    return render(request, "Operaris/operari-realizando.html", context=context)


@login_required()
def operari_finalizado(request):
    template = loader.get_template('Operaris/operari-finalizado.html')

    tasques_operari_finalizado = TaskOperator.objects.filter(finished=True, user=request.user)
    context = {'tasques_operari_finalizado': tasques_operari_finalizado}

    return render(request, "Operaris/operari-finalizado.html", context=context)


def operari_notification(request):
    current_user = request.user.id
    task = Task.objects.filter(user=current_user, hight_priority=True, finished=False)

    if task.exists():
        return HttpResponse(task[0].pk)
    else:
        return HttpResponse("-1")


def operari_detall_tasca(request, pk):
    task = TaskOperator.objects.get(id=pk)
    return render(request, 'Operaris/operari-detall-tasca.html', {'tasca': task})

############################################### TECNIC #################################################################


@login_required()
def tecnics_home(request):
    template = loader.get_template('Tecnics/tecnics-home.html')

    return render(request, "Tecnics/tecnics-home.html")

def CreateAvariaView(request):
    if request.method == 'POST':
        form = CreateAvaria(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('storageandgo:tecnics_home')
    else:
        form = CreateAvaria()
        return render(request, "form.html", {'form': form})



class AvariaList(ListView):
    template_name = 'avaria_list.html'

    def get_context_data(self, **kwargs):
        context = super(AvariaList, self).get_context_data(**kwargs)
        avaria = Avaria.objects.filter(accepted=False, user=requests.user)
        context['task_avaria'] = avaria
        return context

    def get_queryset(self):
        queryset = Avaria.objects.filter()

        return queryset


@login_required()
def tecnics_arealitzar(request):
    template = loader.get_template('Tecnics/tecnics-a-realizar.html')

    tasques_tecnics_a_realitzar = TaskMaintenance.objects.filter(accepted=False)
    context = {'tasques_tecnics_a_realitzar': tasques_tecnics_a_realitzar}

    return render(request, "Tecnics/tecnics-a-realizar.html", context=context)


@login_required()
def tecnics_realizando(request):
    template = loader.get_template('Tecnics/tecnics-realizando.html')

    tasques_tecnics_realizando = TaskMaintenance.objects.filter(accepted=True, finished=False, user=request.user)
    context = {'tasques_tecnics_realizando': tasques_tecnics_realizando}

    return render(request, "Tecnics/tecnics-realizando.html", context=context)


@login_required()
def tecnics_finalizado(request):
    template = loader.get_template('Tecnics/tecnics-finalitzades.html')

    tasques_tecnics_finalitzades = TaskMaintenance.objects.filter(finished=True, user=request.user)
    context = {'tasques_tecnics_finalitzades': tasques_tecnics_finalitzades}

    return render(request, "Tecnics/tecnics-finalitzades.html", context=context)


def tecnics_detall_tasca(request, pk):
    task = TaskMaintenance.objects.get(id=pk)
    return render(request, 'Tecnics/tecnics-detall-tasca.html', {'tasca': task})

################################################# TASKS ################################################################
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
    template_name = 'Gestor_Sala/gestor-sala-a-realizar.html'

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


class ListHistoryTasks(ListView):
    template_name = 'ceo/ceo-history.html'

    def get_context_data(self, **kwargs):
        context = super(ListHistoryTasks, self).get_context_data(**kwargs)
        operator = TaskOperator.objects.filter(finished=True)
        maintenance = TaskMaintenance.objects.filter(finished=True)
        context['task_operator'] = operator
        context['task_maintenance'] = maintenance
        return context

    def get_queryset(self):
        queryset = Task.objects.filter()

        return queryset


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


class TaskUpdate(UpdateView):
    model = Task
    fields = ['user']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskUpdate, self).form_valid(form)


@login_required()
def gestor_registrar_manifest(request):
    template = loader.get_template('gestor_sala_registrar_manifest.html')

    # return HttpResponse(template.render())
    return render(request, "gestor_sala_registrar_manifest.html")


class TaskAccept(UpdateView):
    model = Task
    fields = ['accepted']
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskAccept, self).form_valid(form)


@login_required(login_url='/accounts/login')
def task_accept(request, pk):
    task = Task.objects.get(pk=pk)
    task.accepted = True
    task.user = User.objects.get(username=request.user.username)
    task.save()
    return redirect(request.META.get('HTTP_REFERER'))


@login_required(login_url='/accounts/login')
def task_finish(request, pk):
    group = User.objects.get(username=request.user).groups.all()[0]
    task = Task.objects.get(pk=pk)
    task.finished = True
    task.save()
    if TaskOperator.objects.filter(pk=pk).exists():
        task = TaskOperator.objects.get(pk=pk)
        origin = task.origin
        destination = task.destination

        origin.contenidorsInside -= task.quantity
        destination.contenidorsInside += task.quantity

        origin.save()
        destination.save()
    return redirect(request.META.get('HTTP_REFERER'))


class TaskOperatorModify(UpdateView):
    model = TaskOperator
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user

        super(TaskOperatorModify, self).form_valid(form)

        if self.request.user.groups.all()[0] == "Operari":
            return redirect('storageandgo:operari_home')
        else:
            return redirect('storageandgo:gestor_arealizar')


class TaskMaintenanceModify(UpdateView):
    model = TaskMaintenance
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user

        super(TaskMaintenanceModify, self).form_valid(form)

        if self.request.user.groups.all()[0] == "Tecnic":
            return redirect('storageandgo:tecnics_home')
        else:
            return redirect('storageandgo:gestor_arealizar')


class TaskAvariaModify(UpdateView):
    model = Avaria
    fields = '__all__'
    template_name = "form.html"

    def form_valid(self, form):
        form.instance.sender = self.request.user
        return super(TaskAvariaModify, self).form_valid(form)


@login_required(login_url='/accounts/login')
def CreateOperatorTaskView(request):
    if request.method == "POST":
        form = CreateOperatorTaskForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('storageandgo:gestor_arealizar')

    else:
        form = CreateOperatorTaskForm()
        return render(request, "form.html", {'form': form})


@login_required(login_url='/accounts/login')
def CreateTecnicTaskView(request):
    if request.method == "POST":
        form = CreateTecnicTaskForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return redirect('storageandgo:gestor_arealizar')

    else:
        form = CreateTecnicTaskForm()
        return render(request, "form.html", {'form': form})


# @login_required()
def createTask(contenidor):
    rooms = Room.objects.all()

    avaliable_room = 0
    if rooms:
        for room in rooms:
            if room.temperatureMin > contenidor["tempMinDegree"] and room.temperatureMax < contenidor["tempMaxDegree"] \
                    and room.capacity - room.contenidorsInside > contenidor['qty']:
                avaliable_room = room
                break

        if avaliable_room == 0:
            TaskOperator(description="Mover " + "contenedores de " + contenidor["name"], product=contenidor["name"],
                         origin=Room.objects.all()[0], destination=Room.objects.all()[0], quantity=contenidor["qty"],
                         accepted=False, finished=False, hight_priority=False)

        else:
            task = TaskOperator(description="Mover " + str(contenidor['qty']) + " contenedores de " + contenidor['name'],
                                product=contenidor['name'], origin=Room.objects.all()[0],
                                destination=Room.objects.all()[0], quantity=contenidor['qty'], accepted=False,
                                finished=False, hight_priority=False)
            task.save()
    else:
        ctypes.windll.user32.MessageBoxW(0, "No hay salas disponibles", "Error", 1)


######################################################## Login ###########################################################

def login_success(request):
    if request.user.groups.filter(name="operari").exists():
        # user is an admin
        return redirect("storageandgo:operari_home")
    elif request.user.groups.filter(name="tecnic").exists():
        return redirect("storageandgo:tecnics_home")
    elif request.user.groups.filter(name="gestor").exists():
        return redirect("storageandgo:gestor_arealizar")


######################################################## CEO ###########################################################


class InformeSla(ListView):
    model = Avaria
    template_name = "ceo/document_sla.html"

    def get_context_data(self, **kwargs):
        context = super(InformeSla, self).get_context_data(**kwargs)
        context['manifestos_entrada'] = Manifesto.objects.all().filter(withdrawal=False)
        context['manifestos_sortida'] = Manifesto.objects.all().filter(withdrawal=True)
        context['range'] = reversed(range(1, datetime.date.today().month + 1))
        return context


def complets_sla(request):
    manifestos = Manifesto.objects.all()
    total = 0
    correct = 0
    for manifesto in manifestos:
        for product in manifesto.products.all():
            # print(product.name)
            if manifesto.revisionDate < product.sla:
                correct += 1
            total += 1
    # return HttpResponse(9/100*100)
    return HttpResponse(correct/total*100)


def complets_mes(request):
    month = int(request.GET.get('month', None))
    print(month)

    first = datetime.datetime.now().replace(day=1, month=month)
    last = last_day_of_month(first)
    timezone = pytz.timezone("UTC")
    first = timezone.localize(first)
    last = timezone.localize(last)
    # print(first)
    pass

    manifestos = Manifesto.objects.filter(creationDate__gte=first, creationDate__lte=last)

    total = 0
    correct = 0
    for manifesto in manifestos:
        for product in manifesto.products.all():
            # print(product.name)
            if manifesto.revisionDate < product.sla:
                correct += 1
            total += 1
    # return HttpResponse(9/100*100)
    # return HttpResponse(10 * int(month))
    if total is 0:
        return HttpResponse(-1)
    return HttpResponse(correct / total * 100)


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def capacitat(request):
    rooms = Room.objects.all()
    used = 0
    total = 0
    for room in rooms:
        total += room.capacity
        used += room.contenidorsInside

    # return HttpResponse(50/100*100)
    return HttpResponse(used/total*100)


def sala_detail(request, pk):
    datos = get_object_or_404(Room, pk=pk)
    group = User.objects.get(username=request.user).groups.all()[0]

    context = {'sala': datos}

    if group.name == "Ceo":
        return render(request, 'info_sala2.html', context)
    return render(request, 'info_sala.html', context)


def sala_delete(request, pk):
    try:
        item = get_object_or_404(Room, pk=pk)
        item.delete()
        return redirect(reverse('storageandgo:mapa_salas'))
    except:
        return HttpResponse("Contenedores o Tareas referenciados")
