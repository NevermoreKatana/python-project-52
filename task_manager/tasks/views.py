from django.contrib import messages
from task_manager.tasks.models import Tasks
import rollbar
from task_manager.tasks.forms import TaskForm, TaskFilterForm
from django.views.generic import ListView, CreateView, DeleteView, UpdateView
from django.shortcuts import reverse
from django.http import HttpResponseRedirect
from task_manager.mixins import CustomLoginRequiredMixin, GetSuccessUrlMixin


class IndexView(CustomLoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/index.html'
    context_object_name = 'tasks'

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


class TasksCreateView(CustomLoginRequiredMixin, GetSuccessUrlMixin, CreateView):
    model = Tasks
    template_name = 'tasks/create.html'
    form_class = TaskForm
    success_message = 'Задача успешно создана'
    success_url = 'tasks_index'

    def form_valid(self, form):
        form.instance.author = self.request.user
        rollbar.report_exc_info()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


class TasksDeleteView(CustomLoginRequiredMixin, GetSuccessUrlMixin, DeleteView):
    model = Tasks
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    success_message = 'Задача успешно удалена'
    success_url = 'tasks_index'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.author != self.request.user:
            messages.error(self.request, 'Задачу может удалить только ее автор')
            rollbar.report_exc_info()
            return HttpResponseRedirect(reverse('tasks_index'))
        rollbar.report_exc_info()
        return super().dispatch(request, *args, **kwargs)


class UpdateTaskView(CustomLoginRequiredMixin, GetSuccessUrlMixin, UpdateView):
    model = Tasks
    template_name = 'tasks/update.html'
    form_class = TaskForm
    success_message = 'Задача успешно изменена'
    success_url = 'tasks_index'

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


class TaskView(CustomLoginRequiredMixin, ListView):
    model = Tasks
    template_name = 'tasks/task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = Tasks.objects.get(id=self.kwargs['pk'])
        context['tasks'] = task
        context['form'] = TaskFilterForm(self.request.GET)
        context['is_session_active'] = 'user_id' in self.request.session
        return context
