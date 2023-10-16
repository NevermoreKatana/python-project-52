from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from task_manager.statuses.models import Status
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
import rollbar


class IndexView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            tasks = Tasks.objects.all()
            statuses = Status.objects.all()
            users = User.objects.all()
            labels = Labels.objects.all()

            status_id = request.GET.get('status')
            executor_id = request.GET.get('executor')
            label_id = request.GET.get('label')
            self_tasks = request.GET.get('self_tasks')

            if status_id:
                tasks = tasks.filter(status__id=status_id)
            if executor_id:
                tasks = tasks.filter(executor__id=executor_id)
            if label_id:
                tasks = tasks.filter(labels__id=label_id)

            if self_tasks:
                tasks = tasks.filter(author=request.user)

            return render(request, 'tasks/index.html', {
                'is_session_active': is_session_active,
                'tasks': tasks,
                'statuses': statuses,
                'users': users,
                'labels': labels,
                'status_id': int(status_id) if status_id else status_id,
                'executor_id': int(executor_id) if executor_id else executor_id,
                'label_id': int(label_id) if label_id else label_id,
                'self_tasks': self_tasks,
            })

        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')



class TasksCreateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            statuses = list(Status.objects.all())
            user = User.objects.values('id', 'first_name', 'last_name')
            user = list(user)
            labels = Labels.objects.all()
            rollbar.report_exc_info()
            return render(request, 'tasks/create.html', {'is_session_active': is_session_active, 'statuses': statuses, 'user': user, 'labels': labels})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        executor = request.POST.get('executor')
        labels = request.POST.getlist('labels')
        task = Tasks()
        task.name = name
        task.description = description
        task.status = Status.objects.get(id=status)
        task.executor = User.objects.get(id=executor)
        task.author = User.objects.get(id=request.session.get('user_id'))
        task.save()
        for label_id in labels:
            label = Labels.objects.get(id=label_id)
            task.labels.add(label)
        rollbar.report_exc_info()
        messages.success(request, 'Задача успешно создана')
        return redirect('tasks_index')


class TasksDeleteView(View):

    def get(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if is_session_active:
            task = Tasks.objects.values('name', 'author').filter(id=task_id)
            if request.session.get('user_id') != task[0]['author']:
                messages.error(request, 'Задачу может удалить только ее автор')
                rollbar.report_exc_info()
                return redirect('tasks_index')
            task = list(task)
            rollbar.report_exc_info()
            return render(request, 'tasks/delete.html', {'is_session_active': is_session_active, 'task': task[0]})
        rollbar.report_exc_info()
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return redirect('login')

    def post(self, request, *args, **kwargs):
        task_id = kwargs.get('pk')
        task = Tasks.objects.get(id=task_id)
        if task:
            task.delete()
            messages.error(request, 'Задача успешно удалена')
            rollbar.report_exc_info()
            return redirect('tasks_index')


class UpdateStatusView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        if is_session_active:
            task_id = kwargs.get('pk')
            statuses = list(Status.objects.all())
            user = User.objects.values('id', 'first_name', 'last_name')
            user = list(user)
            labels = Labels.objects.all()
            task = Tasks.objects.get(id=task_id)
            rollbar.report_exc_info()
            return render(request, 'tasks/update.html', {'is_session_active': is_session_active, 'statuses': statuses, 'user': user, 'task': task, 'labels': labels})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')

    def post(self, request, *args, **kwargs):
        status_id = kwargs.get('pk')
        name = request.POST.get('name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        executor = request.POST.get('executor')
        labels = request.POST.getlist('labels')
        task = Tasks.objects.get(id=status_id)
        task.name = name
        task.description = description
        task.status = Status.objects.get(id=status)
        task.executor = User.objects.get(id=executor)
        task.author = User.objects.get(id=request.session.get('user_id'))
        task.labels.clear()
        task.save()
        for label_id in labels:
            label = Labels.objects.get(id=label_id)
            task.labels.add(label)

        messages.success(request, 'Задача успешно изменена')
        rollbar.report_exc_info()
        return redirect('tasks_index')


class TaskView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        task_id = kwargs.get('pk')
        if is_session_active:
            tasks = Tasks.objects.get(id=task_id)
            rollbar.report_exc_info()
            return render(request, 'tasks/task.html', {'is_session_active': is_session_active, 'tasks': tasks})
        messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return redirect('login')
