from django import forms
from task_manager.labels.models import Labels

class LabelForm(forms.Form):
    class Meta:
        model = Labels
        fields = ['name']
        label = 'Имя',
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя',
                'required': 'required',
            }),
        }
