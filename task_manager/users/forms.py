from django import forms


class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label='Имя',
        label_suffix='',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя',
            'required': 'required',
            'id': 'id_first_name'
        })
    )

    last_name = forms.CharField(
        label='Фамилия',
        label_suffix='',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Фамилия',
            'required': 'required',
            'id': 'id_last_name'
        })
    )

    username = forms.CharField(
        label='Имя пользователя',
        label_suffix='',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': 'required',
            'id': 'id_username'
        })
    )

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
