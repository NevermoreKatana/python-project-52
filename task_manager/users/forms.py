from django import forms
from django.contrib.auth import get_user_model



class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': ("Пароль и подтверждение пароля не совпадают."),
    }
    password1 = forms.CharField(
        label='Пароль',
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Пароль',
            'required': True,
            'id': 'id_password1'
        })
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        label_suffix='',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Подтверждение пароля',
            'required': True,
            'id': 'id_password2'
        })
    )

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "username")
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                                 'placeholder': 'Имя',
                                                 'required': True,
                                                 'id': 'id_first_name'}
                                          ),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                                'placeholder': 'Фамилия',
                                                'required': True,
                                                'id': 'id_last_name'}
                                         ),
            'username': forms.TextInput(attrs={'class': 'form-control',
                                               'placeholder': 'Имя пользователя',
                                               'required': True,
                                               'id': 'id_username'}
                                        )
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

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
