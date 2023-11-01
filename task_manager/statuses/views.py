from task_manager.statuses.models import Status
from django.contrib import messages
import rollbar
from task_manager.statuses.forms import StatusForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse
from task_manager.mixins import CustomLoginRequiredMixin, GetSuccessUrlMixin


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


class CreateStatusView(CustomLoginRequiredMixin, GetSuccessUrlMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    form_class = StatusForm
    success_message = 'Статус успешно создан'
    custom_success_url = 'statuses_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context



class UpdateStatusView(CustomLoginRequiredMixin, GetSuccessUrlMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = StatusForm
    success_message = 'Статус успешно изменен'
    custom_success_url = 'statuses_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        satus = Status.objects.get(id=self.kwargs['pk'])
        initial_data = {
            'name': satus.name,
        }

        kwargs['initial'] = initial_data
        return kwargs


class DeleteStatusView(CustomLoginRequiredMixin,GetSuccessUrlMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'
    success_message = 'Статус успешно удален'
    custom_success_url = 'statuses_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context
