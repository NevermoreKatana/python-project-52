from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Имя',
                                                 'required': 'required',
                                                 'id': 'id_first_name'}
                                          ),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Фамилия',
                                                'required': 'required',
                                                'id': 'id_last_name'}
                                         ),
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Имя пользователя',
                                               'required': 'required',
                                               'id': 'id_username'}
                                        )
        }
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'username': 'Имя пользователя',
        }

    password1 = forms.CharField(
        label='Пароль',
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'required': 'required',
            'id': 'id_password1'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'required': 'required',
            'id': 'id_password2'
        })
    )
