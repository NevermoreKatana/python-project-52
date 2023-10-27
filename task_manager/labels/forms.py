from django import forms
from task_manager.labels.models import Labels


class LabelForm(forms.ModelForm):
    class Meta:
        model = Labels
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
        }
        labels = {
            'name': 'Имя',
        }
