from django.forms import ModelForm
from .models import *


class CreateTaskForm(ModelForm):
    class Meta:
        model = TaskOperator
        fields = '__all__'
