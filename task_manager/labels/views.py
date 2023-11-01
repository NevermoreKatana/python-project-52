from django.contrib import messages
from task_manager.labels.models import Labels
import rollbar
from task_manager.labels.forms import LabelForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from task_manager.mixins import CustomLoginRequiredMixin


class LabelsView(CustomLoginRequiredMixin, ListView):
    model = Labels
    template_name = 'labels/index.html'
    context_object_name = 'labels'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context



class LabelsCreateView(CustomLoginRequiredMixin, CreateView):
    model = Labels
    template_name = 'labels/create.html'
    form_class = LabelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Метка успешно создана')
        rollbar.report_exc_info()
        return reverse('labels_index')


    def post(self, request, *args, **kwargs):
        name = self.request.POST.get('name')

        if Labels.objects.filter(name=name).exists():
            messages.error(self.request, 'Label с таким именем уже существует.')
            rollbar.report_exc_info()
            return HttpResponseRedirect(reverse('labels_create'))
        rollbar.report_exc_info()
        return super().post(request, *args, **kwargs)


class LabelsDeleteView(CustomLoginRequiredMixin, DeleteView):
    model = Labels
    template_name = 'labels/delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Метка успешно удалена')
        rollbar.report_exc_info()
        return reverse('labels_index')



class LabelsUpdateView(CustomLoginRequiredMixin, UpdateView):
    model = Labels
    template_name = 'statuses/update.html'
    form_class = LabelForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_success_url(self):
        messages.success(self.request, 'Метка успешно изменена')
        rollbar.report_exc_info()
        return reverse('labels_index')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        label = Labels.objects.get(id=self.kwargs['pk'])
        initial_data = {
            'name': label.name,
        }

        kwargs['initial'] = initial_data
        return kwargs
