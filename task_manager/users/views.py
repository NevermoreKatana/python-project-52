from django.contrib.auth.models import User
from django.contrib.auth import logout
from task_manager.tasks.models import Tasks
import rollbar
from task_manager.users.forms import RegistrationForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from task_manager.mixins import CustomLoginRequiredMixin, GetSuccessUrlMixin
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

class UserView(ListView):
    model = get_user_model()
    template_name = 'users/index.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


class UserCreateView(CreateView, GetSuccessUrlMixin):
    model = get_user_model()
    template_name = 'users/create.html'
    form_class = RegistrationForm
    success_message = ''
    success_url = '/login/'


    def form_valid(self, form):
        password = form.cleaned_data['password1']
        password_confirm = form.cleaned_data['password2']

        if password != password_confirm:
            messages.error(self.request, "Пароль и подтверждение пароля не совпадают.")
            rollbar.report_exc_info()
            return self.form_invalid(form)

        form.instance.password = make_password(password)
        messages.success(self.request, 'Пользователь успешно зарегистрирован')
        rollbar.report_exc_info()
        return super().form_valid(form)


class UserDeleteView(CustomLoginRequiredMixin, GetSuccessUrlMixin, DeleteView):
    model = get_user_model()
    template_name = 'users/delete.html'
    success_message = 'Пользователь успешно удален'
    success_url = '/users/'
    logout = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.id != self.request.user.id:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
            rollbar.report_exc_info()
            return HttpResponseRedirect(reverse('users_index'))
        rollbar.report_exc_info()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        if Tasks.objects.filter(executor=user) or Tasks.objects.filter(author=user):
            messages.error(self.request,
                           'Невозможно удалить пользователя, потому что он используется')
            rollbar.report_exc_info()
            return HttpResponseRedirect(reverse('users_index'))
        rollbar.report_exc_info()
        return super().post(request, *args, **kwargs)


class UserUpdateView(CustomLoginRequiredMixin, GetSuccessUrlMixin, UpdateView):
    model = get_user_model()
    template_name = 'users/update.html'
    form_class = RegistrationForm
    success_message = 'Пользователь успешно изменен'
    success_url = 'users_index'
    logout = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


    def dispatch(self, request, *args, **kwargs):
        user = self.get_object()
        if user.id != self.request.user.id:
            messages.error(self.request, 'У вас нет прав для изменения другого пользователя.')
            rollbar.report_exc_info()
            return HttpResponseRedirect(reverse('users_index'))
        rollbar.report_exc_info()
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        password = form.cleaned_data['password1']
        password_confirm = form.cleaned_data['password2']

        if password != password_confirm:
            messages.error(self.request, "Пароль и подтверждение пароля не совпадают.")
            rollbar.report_exc_info()
            return self.form_invalid(form)
        rollbar.report_exc_info()
        form.instance.password = make_password(password)
        return super().get_success_url()
