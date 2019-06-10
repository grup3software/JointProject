from django.forms import ModelForm
from .models import *


class CreateOperatorTaskForm(ModelForm):
    class Meta:
        model = TaskOperator
        fields = '__all__'


class CreateTecnicTaskForm(ModelForm):
    class Meta:
        model = TaskMaintenance
        fields = '__all__'


class CreateSala(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ('contenidorsInside',)

class CreateAvaria(ModelForm):
    class Meta:
        model = Avaria
        fields = 'object', 'room','high_priority'
