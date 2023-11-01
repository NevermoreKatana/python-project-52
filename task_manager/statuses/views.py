from task_manager.statuses.models import Status
from django.contrib import messages
import rollbar
from task_manager.statuses.forms import StatusForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse
from task_manager.mixins import CustomLoginRequiredMixin


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


class CreateStatusView(CustomLoginRequiredMixin, CreateView):
    model = Status
    template_name = 'statuses/create.html'
    form_class = StatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно создан')
        rollbar.report_exc_info()
        return reverse('statuses_index')



class UpdateStatusView(CustomLoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    form_class = StatusForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно изменен')
        rollbar.report_exc_info()
        return reverse('statuses_index')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        satus = Status.objects.get(id=self.kwargs['pk'])
        initial_data = {
            'name': satus.name,
        }

        kwargs['initial'] = initial_data
        return kwargs


class DeleteStatusView(CustomLoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Статус успешно удален')
        rollbar.report_exc_info()
        return reverse('statuses_index')

