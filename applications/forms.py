from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job', 'resume_summary']
        widgets = {
            'job': forms.HiddenInput()
        }
