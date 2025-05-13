from django import forms
from .models import TaskReport

class TaskReportForm(forms.ModelForm):
    class Meta:
        model = TaskReport
        fields = ['date', 'topic']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'topic': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter today\'s work...'}),
        }
