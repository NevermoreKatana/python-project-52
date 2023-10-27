from django.contrib import messages
from task_manager.statuses.models import Status
from task_manager.tasks.models import Tasks
import rollbar
from task_manager.tasks.forms import TaskForm, TaskFilterForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import reverse
from django.http import HttpResponseRedirect


class IndexView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'
    login_url = 'login'
    redirect_field_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            status = form.cleaned_data['status']
            executor = form.cleaned_data['executor']
            label = form.cleaned_data['label']
            self_tasks = form.cleaned_data['self_tasks']
            if status:
                queryset = queryset.filter(status__id=status)
            if executor:
                queryset = queryset.filter(executor__id=executor)
            if label:
                queryset = queryset.filter(labels__id=label)
            if self_tasks:
                queryset = queryset.filter(author=self.request.user)
        return queryset

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()


class TasksCreateView(LoginRequiredMixin, CreateView):
    model = Tasks
    template_name = 'tasks/create.html'
    form_class = TaskForm
    login_url = 'login'

    def get_success_url(self):
        return reverse('tasks_index')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Задача успешно создана')
        return super().form_valid(form)

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context



class TasksDeleteView(LoginRequiredMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()

    def get_success_url(self):
        messages.success(self.request, 'Задача успешно удалена')
        return reverse('tasks_index')

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != self.request.user:
            messages.error(self.request, 'Задачу может удалить только ее автор')
            return HttpResponseRedirect(reverse('tasks_index'))
        return super().dispatch(request, *args, **kwargs)

class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/update.html'
    form_class = TaskForm
    login_url = 'login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        task = Tasks.objects.get(id=self.kwargs['pk'])
        label_ids = list(task.labels.values_list('id', flat=True))
        initial_data = {
            'name': task.name,
            'description': task.description,
            'status_id': task.status.id,
            'executor_id': task.executor.id,
            'labels': label_ids
        }

        kwargs['initial'] = initial_data
        return kwargs

    def get_success_url(self):
        messages.success(self.request, 'Задача успешно изменена')
        return reverse('tasks_index')

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()



class TaskView(LoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/task.html'
    login_url = 'login'
    redirect_field_name = ""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Tasks.objects.get(id=self.kwargs['pk'])
        context['tasks'] = task
        context['form'] = TaskFilterForm(self.request.GET)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        return super().handle_no_permission()

