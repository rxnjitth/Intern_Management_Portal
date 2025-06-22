from django import forms
from .models import TaskReport

class TaskReportForm(forms.ModelForm):
    class Meta:
        model = TaskReport
        fields = ['topic']  # exclude 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].widget.attrs.update({'placeholder': 'Enter your task for today'})
