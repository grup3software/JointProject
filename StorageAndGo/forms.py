from django.forms import ModelForm
from .models import *


class CreateTaskForm(ModelForm):
    class Meta:
        model = TaskOperator
        fields = '__all__'


class CreateSala(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'

