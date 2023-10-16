from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from task_manager.labels.models import Labels
from task_manager.tasks.models import Tasks
import rollbar


class LabelsView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            labels = list(Labels.objects.all())
            rollbar.report_exc_info()
            return render(request, 'labels/index.html',
                          {'is_session_active': is_session_active,
                           'labels': labels})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')


class LabelsCreateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            rollbar.report_exc_info()
            return render(request, 'labels/create.html', {'is_session_active': is_session_active})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        task = Labels()
        task.name = name
        task.save()
        rollbar.report_exc_info()
        messages.success(request, 'Метка успешно создана')
        return redirect('labels_index')


class LabelsDeleteView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if is_session_active:
            label = Labels.objects.values('name').filter(id=task_id)
            label = list(label)
            rollbar.report_exc_info()
            return render(request, 'labels/delete.html',
                          {'is_session_active': is_session_active,
                           'label': label[0]})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        label = Labels.objects.get(id=task_id)
        if Tasks.objects.filter(labels=label):
            messages.error(request, 'Невозможно удалить метку, потому что она используется')
            rollbar.report_exc_info()
            return redirect('labels_index')

        label.delete()
        messages.error(request, 'Метка успешно удалена')
        rollbar.report_exc_info()
        return redirect('labels_index')


class LabelsUpdateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            label_id = kwargs.get('pk')
            label = Labels.objects.get(id=label_id)
            rollbar.report_exc_info()
            return render(request, 'labels/update.html',
                          {'is_session_active': is_session_active,
                           'label': label})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        name = request.POST.get('name')
        task = Labels.objects.get(id=status_id)
        task.name = name
        task.save()
        messages.success(request, 'Метка успешно изменена')
        rollbar.report_exc_info()
        return redirect('labels_index')
