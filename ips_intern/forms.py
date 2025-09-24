from django import forms
from .models import *

class TaskReportForm(forms.ModelForm):
    class Meta:
        model = TaskReport
        fields = ['topic']  # exclude 'date'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['topic'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': ' ',
            'id': 'taskTopicField',
            'rows': '5'
        })

class InternApplicationForm(forms.ModelForm):
    class Meta:
        model = InternApplication
        exclude = ['user', 'is_certified', 'is_approved', 'is_rejected', 'just_approved', 'is_completed']
