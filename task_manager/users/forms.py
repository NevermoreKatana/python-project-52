from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'required': 'required',
            'id': 'id_first_name'
        }),
            'last_name': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
            'required': 'required',
            'id': 'id_last_name'
        }),
            'username': forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': 'required',
            'id': 'id_username'
        }),
            'password': forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'required': 'required',
            'id': 'id_password'
        }),
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
            'password': 'Пароль'
        }

    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'required': 'required',
            'id': 'password_confirm'
        })
    )