from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from task_manager.labels.models import Labels
from task_manager.tasks.models import Tasks
import rollbar
from task_manager.labels.forms import LabelForm
from task_manager.labels import services
from task_manager.services import handle_success, handle_error

class LabelsView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            labels = list(Labels.objects.all().order_by('id'))
            rollbar.report_exc_info()
            return render(request, 'labels/index.html',
                          {'is_session_active': is_session_active,
                           'labels': labels})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

class LabelsCreateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        form = LabelForm()
        if is_session_active:
            rollbar.report_exc_info()
            return render(request, 'labels/create.html', {'is_session_active': is_session_active, 'form':form})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):
        form = LabelForm(request.POST)
        if services.create_label(form):
            return handle_success(request, 'Метка успешно создана', 'labels_index')


class LabelsDeleteView(View):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if is_session_active:
            label = services.get_label_info(label_id)
            rollbar.report_exc_info()
            return render(request, 'labels/delete.html',
                          {'is_session_active': is_session_active,
                           'label': label[0]})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        if services.delete_label(label_id):
            return handle_success(request, 'Метка успешно удалена', 'labels_index')
        return handle_error(request, 'Невозможно удалить метку, потому что она используется','labels_index')


class LabelsUpdateView(View):

    def get(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if is_session_active:
            label = services.get_initial_data(label_id)
            form = LabelForm(label)
            rollbar.report_exc_info()
            return render(request, 'labels/update.html',
                          {'is_session_active': is_session_active,
                           'form': form})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):
        label_id = kwargs.get('pk')
        form = LabelForm(request.POST)
        if services.update_label(form, label_id):
            return handle_success(request, 'Метка успешно изменена', 'labels_index')

