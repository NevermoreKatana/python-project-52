from django import forms
from task_manager.statuses.models import Status
from task_manager.labels.models import Labels
from django.contrib.auth.models import User

class TaskForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}))
    description = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}))
    status = forms.ChoiceField(label='Статус', choices=[], widget=forms.Select(attrs={'class': 'form-select'}))
    executor = forms.ChoiceField(label='Исполнитель', choices=[], widget=forms.Select(attrs={'class': 'form-select'}))
    labels = forms.MultipleChoiceField(label='Метки', choices=[], widget=forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': 'multiple'}))

    def __init__(self, *args, **kwargs):
        name = kwargs.pop('name', None)
        description = kwargs.pop('description', None)
        status_id = kwargs.pop('status_id', None)
        executor_id = kwargs.pop('executor_id', None)
        labels = kwargs.pop('labels', None)

        super(TaskForm, self).__init__(*args, **kwargs)

        self.fields['status'].choices = [('', '---------')] + [(status.id, status.name) for status in Status.objects.all()]
        self.fields['executor'].choices = [('', '---------')] + [(executor.id, f"{executor.first_name} {executor.last_name}") for executor in
                                           User.objects.all()]
        self.fields['labels'].choices = [(label.id, label.name) for label in Labels.objects.all()]

        if name:
            self.initial['name'] = name

        if description:
            self.initial['description'] = description

        if status_id:
            self.initial['status'] = status_id

        if executor_id:
            self.initial['executor'] = executor_id

        if labels:
            self.initial['labels'] = labels


class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        label='Статус',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select '})
    )
    executor = forms.ChoiceField(
        label='Исполнитель',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select '})
    )
    label = forms.ChoiceField(
        label='Метка',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select '})
    )
    self_tasks = forms.BooleanField(
        label='Только свои задачи',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)

        self.fields['status'].choices = [('', '---------')] + [(status.id, status.name) for status in Status.objects.all()]
        self.fields['executor'].choices = [('', '---------')] + [(u.id, f"{u.first_name} {u.last_name}") for u in User.objects.all()]
        self.fields['labels'].choices = [('', '---------')] + [(label.id, label.name) for label in Labels.objects.all()]


