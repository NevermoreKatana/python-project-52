from django.shortcuts import render, redirect
from django.views import View
from task_manager.statuses.models import Status
from django.contrib import messages
import rollbar


class IndexView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            statuses = Status.objects.all()
            rollbar.report_exc_info()
            return render(request, 'statuses/index.html', {'is_session_active': is_session_active, 'statuses': statuses})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')


class CreateStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            rollbar.report_exc_info()
            return render(request, 'statuses/create.html', {'is_session_active': is_session_active})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        status = Status()
        status.name = name
        status.save()
        rollbar.report_exc_info()
        messages.success(request, 'Статус успешно создан')
        return redirect('statuses_index')


class UpdateStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            status_id = kwargs.get('pk')
            status = Status.objects.get(id=status_id)
            rollbar.report_exc_info()
            return render(request, 'statuses/update.html', {'is_session_active': is_session_active, 'status': status})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        name = request.POST.get('name')
        status = Status.objects.get(id=status_id)
        status.name = name
        status.save()
        rollbar.report_exc_info()
        return redirect('statuses_index')


class DeleteStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            status_id = kwargs.get('pk')
            status = Status.objects.get(id=status_id)
            rollbar.report_exc_info()
            return render(request, 'statuses/delete.html', {'is_session_active': is_session_active, 'status': status})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        status = Status.objects.get(id=status_id)
        status.delete()
        rollbar.report_exc_info()
        return redirect('statuses_index')
