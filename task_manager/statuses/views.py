from django.shortcuts import render, redirect
from django.views import View
from task_manager.statuses.models import Status
from django.contrib import messages
import rollbar
from task_manager.statuses.forms import StatusForm
from task_manager.services import handle_error, handle_success
from task_manager.statuses import services
from django.views.generic import ListView

class IndexView(ListView):
    model = Status
    template_name = 'statuses/index.html'
    context_object_name = 'statuses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context
    #     messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
    #     rollbar.report_exc_info()
    #     return redirect('login')


class CreateStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        form = StatusForm()
        if is_session_active:
            rollbar.report_exc_info()
            return render(request, 'statuses/create.html', {'is_session_active': is_session_active, 'form': form})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')
    def post(self, request, *args, **kwargs):
        form = StatusForm(request.POST)
        if services.create_status(form):
            return handle_success(request, 'Статус успешно создан', 'statuses_index')


class UpdateStatusView(View):

    def get(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if is_session_active:
            initial_data = services.get_initial_data(status_id)
            form = StatusForm(initial_data)
            rollbar.report_exc_info()
            return render(request, 'statuses/update.html',
                          {'is_session_active': is_session_active,
                           'form': form})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        form = StatusForm(request.POST)
        if services.update_status(status_id, form):
            return handle_success(request, 'Статус успешно изменен','statuses_index')


class DeleteStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            status_id = kwargs.get('pk')
            status = Status.objects.get(id=status_id)
            rollbar.report_exc_info()
            return render(request, 'statuses/delete.html',
                          {'is_session_active': is_session_active,
                           'status': status})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):

        status_id = kwargs.get('pk')
        services.delete_status(status_id)
        return handle_success(request, 'Статус успешно удален', 'statuses_index')
