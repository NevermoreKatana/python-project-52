from django.shortcuts import render, redirect
from django.views import View
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import logout
from task_manager.validator import password_validate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from task_manager.statuses.models import Status
from task_manager.tasks.models import Tasks

class IndexView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            tasks = Tasks.objects.all()
            statuses = Status.objects.all()
            users = User.objects.all()
            return render(request, 'tasks/index.html', {'is_session_active':request.session.get('user_id'), 'tasks':tasks, 'statuses':statuses,'users':users })
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')


class TasksCreateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            statuses = list(Status.objects.all())
            user = User.objects.values('id', 'first_name', 'last_name')
            user = list(user)
            return render(request, 'tasks/create.html', {'is_session_active':is_session_active, 'statuses': statuses, 'user':user})
        messages.error(request,'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        executor = request.POST.get('executor')
        labels = request.POST.get('labels')
        task = Tasks()
        task.name = name
        task.description = description
        task.status = Status.objects.get(id=status)
        task.executor = User.objects.get(id=executor)
        task.labels = labels
        task.author = User.objects.get(id=request.session.get('user_id'))
        task.save()
        return redirect('tasks_index')

class TasksDeleteView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if is_session_active:
            task = Tasks.objects.values('name', 'author').filter(id=task_id)
            if request.session.get('user_id') != task[0]['author']:
                messages.error(request, 'Задачу может удалить только ее автор')
                return redirect('tasks_index')
            task = list(task)
            return render(request, 'tasks/delete.html', {'is_session_active': is_session_active, 'task': task[0]})

        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')


    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Tasks.objects.get(id=task_id)
        if task:
            task.delete()
            messages.success(request, 'Задача успешно удалена')
            return redirect('tasks_index')


class UpdateStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            task_id = kwargs.get('pk')
            statuses = list(Status.objects.all())
            user = User.objects.values('id', 'first_name', 'last_name')
            user = list(user)
            task = Tasks.objects.get(id=task_id)
            return render(request, 'tasks/update.html', {'is_session_active': is_session_active, 'statuses':statuses, 'user':user, 'task':task})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        executor = request.POST.get('executor')
        labels = request.POST.get('labels')
        task = Tasks.objects.get(id=status_id)
        task.name = name
        task.description = description
        task.status = Status.objects.get(id=status)
        task.executor = User.objects.get(id=executor)
        task.labels = labels
        task.author = User.objects.get(id=request.session.get('user_id'))
        task.save()
        messages.success(request, 'Задача успешно изменена')
        return redirect('tasks_index')


class TaskView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        task_id = kwargs.get('pk')
        if is_session_active:
            tasks = Tasks.objects.get(id=task_id)
            return render(request, 'tasks/task.html', {'is_session_active':request.session.get('user_id'), 'tasks':tasks})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')
