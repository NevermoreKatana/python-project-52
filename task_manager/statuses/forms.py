from django import forms
from task_manager.statuses.models import Status

class StatusForm(forms.Form):
    class Meta:
        model = Status
        fields = ['name']
        label='Имя',
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'required': 'required',
            }),
        }
