from django import forms
from django.forms import ModelForm
from models import Project


class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'jira_name', 'active', 'complete']
        #exclude = ('created', 'score')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'jira_name': forms.TextInput(attrs={'class': 'form-control'})
        }
