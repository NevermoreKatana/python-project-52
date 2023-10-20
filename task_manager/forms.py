from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        label_suffix='',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Имя пользователя',
            'required': 'required',
        }
        ),
    )
    password = forms.CharField(
        label='Пароль',
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'required': 'required'}),
    )

    def __init__(self, *args, **kwargs):
        is_valid = kwargs.pop('is_valid', False)
        super(LoginForm, self).__init__(*args, **kwargs)
        if is_valid:
            self.fields['username'].widget.attrs['class'] += ' is-valid'
            self.fields['password'].widget.attrs['class'] += ' is-valid'
