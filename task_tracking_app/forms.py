from django import forms
from .models import Task, Comment

class TaskForm(forms.ModelForm):
    due_date = forms.DateInput(attrs={'type': 'date'})
    
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES, widget=forms.Select())
    priority = forms.ChoiceField(choices=Task.PRIORITY_CHOICES, widget=forms.Select())
    
    class Meta:
        model = Task
        fields = ("title", "description", "status", "priority", 'files', 'deadline')
        widgets = {
            'files': forms.FileInput(),
            'deadline': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['files'].required = False

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']