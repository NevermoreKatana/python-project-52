from django import forms


class StatusForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        label_suffix='',
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'required': 'required',
        }))
