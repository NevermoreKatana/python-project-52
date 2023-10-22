from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from task_manager.statuses.models import Status
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
import rollbar
from task_manager.services import handle_success, handle_error
from task_manager.tasks import services
from task_manager.tasks.forms import TaskForm, TaskFilterForm

class IndexView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            form = TaskFilterForm(request.GET)
            tasks = services.task_filter(form, request)
            return render(request, 'tasks/index.html', {
                'is_session_active': is_session_active,
                'tasks': tasks,
                'form': form,
            })

        return handle_error(request,'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

class TasksCreateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            form = TaskForm()
            rollbar.report_exc_info()
            return render(request, 'tasks/create.html',
                          {'is_session_active': is_session_active,
                           'form': form})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):
        form = TaskForm(request.POST)
        if services.create_task(form, request):
            return handle_success(request, 'Задача успешно создана','tasks_index')


class TasksDeleteView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if is_session_active:
            task = services.not_author_delete(request, task_id)
            if task:
                rollbar.report_exc_info()
                return render(request, 'tasks/delete.html',
                              {'is_session_active': is_session_active,
                               'task': task})
            return handle_error(request, 'Задачу может удалить только ее автор', 'tasks_index')
        return handle_error(request,'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        if services.delete_task(task_id):
            return handle_success(request, 'Задача успешно удалена', 'tasks_index')


class UpdateStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        task_id = kwargs.get('pk')
        if is_session_active:
            form = services.get_init_update_task(task_id)
            rollbar.report_exc_info()
            return render(request, 'tasks/update.html',
                          {'is_session_active': is_session_active,
                           'form': form})
        return handle_error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        form = TaskForm(request.POST)
        if services.update_task(task_id, form, request):
            return handle_success(request, 'Задача успешно изменена', 'tasks_index')


class TaskView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        task_id = kwargs.get('pk')
        if is_session_active:
            tasks = Tasks.objects.get(id=task_id)
            rollbar.report_exc_info()
            return render(request, 'tasks/task.html',
                          {'is_session_active': is_session_active,
                           'tasks': tasks})
        return handle_error(request,'Вы не авторизованы! Пожалуйста, выполните вход.', 'login')
