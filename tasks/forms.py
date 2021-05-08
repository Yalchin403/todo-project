from django import forms
from django.forms import ModelForm
from .models import *


class TaskForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'done']
        widgets = {
            'title': forms.TextInput(attrs={"class":"form-control"}),
            'description': forms.Textarea(attrs={"class":"form-control"}),
            'deadline': forms.DateTimeInput(attrs={"class":"form-control"})
        }