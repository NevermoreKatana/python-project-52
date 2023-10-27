from task_manager.statuses.models import Status
from django.contrib import messages
import rollbar
from task_manager.statuses.forms import StatusForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse


class IndexView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'
    login_url = 'login'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()


class CreateStatusView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    form_class = StatusForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно создан')
        return reverse('statuses_index')

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()



class UpdateStatusView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = StatusForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно изменен')
        return reverse('statuses_index')

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        satus = Status.objects.get(id=self.kwargs['pk'])
        initial_data = {
            'name': satus.name,
        }

        kwargs['initial'] = initial_data
        return kwargs



class DeleteStatusView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно удален')
        return reverse('statuses_index')

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()
