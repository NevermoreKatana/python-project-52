from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': 'required'}),
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control {% if messages %}{% for message in messages %}{% if "info" in message.tags %}is-valid{% endif %}{% endfor %}{% endif %}',
            'placeholder': 'Пароль',
            'required': 'required'}),
    )
