from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    due_date = forms.DateInput(attrs={'type': 'date'})
    
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES, widget=forms.Select())
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES, widget=forms.Select())
    

    class Meta:
        model = Task
        fields = ("title", "description", "due_date", "status", "priority")
