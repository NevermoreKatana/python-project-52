from django.contrib import messages
from task_manager.labels.models import Labels
import rollbar
from task_manager.labels.forms import LabelForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from task_manager.mixins import CustomLoginRequiredMixin, GetSuccessUrlMixin, GetContextDataMixin


class LabelsView(CustomLoginRequiredMixin, ListView, GetContextDataMixin):
    model = Labels
    template_name = 'labels/index.html'
    context_object_name = 'labels'


class LabelsCreateView(CustomLoginRequiredMixin,
                       GetSuccessUrlMixin,
                       CreateView,
                       GetContextDataMixin):
    model = Labels
    template_name = 'labels/create.html'
    form_class = LabelForm
    success_message = 'Метка успешно создана'
    success_url = 'labels_index'

    def post(self, request, *args, **kwargs):
        name = self.request.POST.get('name')

        if Labels.objects.filter(name=name).exists():
            messages.error(self.request, 'Label с таким именем уже существует.')
            rollbar.report_exc_info()
            return HttpResponseRedirect(reverse('labels_create'))
        rollbar.report_exc_info()
        return super().post(request, *args, **kwargs)


class LabelsDeleteView(CustomLoginRequiredMixin,
                       GetSuccessUrlMixin,
                       DeleteView,
                       GetContextDataMixin):
    model = Labels
    template_name = 'labels/delete.html'
    success_message = 'Метка успешно удалена'
    success_url = 'labels_index'


class LabelsUpdateView(CustomLoginRequiredMixin,
                       GetSuccessUrlMixin,
                       UpdateView,
                       GetContextDataMixin):
    model = Labels
    template_name = 'statuses/update.html'
    form_class = LabelForm
    success_message = 'Метка успешно изменена'
    success_url = 'labels_index'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        label = Labels.objects.get(id=self.kwargs['pk'])
        initial_data = {
            'name': label.name,
        }

        kwargs['initial'] = initial_data
        return kwargs
