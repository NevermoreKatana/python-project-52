from task_manager.statuses.models import Status
from task_manager.tasks.models import Tasks
from task_manager.labels.models import Labels
from django.contrib.auth.models import User
from task_manager.tasks.forms import TaskForm


def create_task(form, request):
    if form.is_valid():
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        status = form.cleaned_data['status']
        executor = form.cleaned_data['executor']
        labels = form.cleaned_data['labels']
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
        return True
    return False


def not_author_delete(request, task_id):
    task = Tasks.objects.values('name', 'author').filter(id=task_id)
    if not request.session.get('user_id') != task[0]['author']:
        task = list(task)
        return task[0]
    return False


def delete_task(task_id):
    task = Tasks.objects.get(id=task_id)
    if task:
        task.delete()
        return True
    return False


def get_init_update_task(task_id):
    task = Tasks.objects.get(id=task_id)
    label_ids = list(task.labels.values_list('id', flat=True))
    form = TaskForm(name=task.name, description=task.description, status_id=task.status.id, executor_id=task.executor.id, labels=label_ids)
    return form


def update_task(task_id, form, request):
    task = Tasks.objects.get(id=task_id)
    if form.is_valid():
        name = form.cleaned_data['name']
        description = form.cleaned_data['description']
        status = form.cleaned_data['status']
        executor = form.cleaned_data['executor']
        labels = form.cleaned_data['labels']
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
        return True
    return False


def task_filter(form, request):
    tasks = Tasks.objects.all()
    if form.is_valid():
        status = form.cleaned_data['status']
        executor = form.cleaned_data['executor']
        label = form.cleaned_data['label']
        self_tasks = form.cleaned_data['self_tasks']
        if status:
            tasks = tasks.filter(status__id=status)
        if executor:
            tasks = tasks.filter(executor__id=executor)
        if label:
            tasks = tasks.filter(labels__id=label)
        if self_tasks:
            tasks = tasks.filter(author=request.user)
    return tasks
