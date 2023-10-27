from django import forms
from task_manager.statuses.models import Status
from task_manager.labels.models import Labels
from django.contrib.auth.models import User
from task_manager.tasks.models import Tasks
class TaskForm(forms.ModelForm):
    class Meta:
        model = Tasks
        fields = ['name', 'description', 'status', 'executor', 'labels']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'executor': forms.Select(attrs={'class': 'form-select', 'required': False}),
            'labels': forms.SelectMultiple(attrs={'class': 'form-select', 'multiple': 'multiple', 'required': False}),
        }
        labels = {
            'name': 'Имя',
            'description': 'Описание',
            'status': 'Статус',
            'executor': 'Исполнитель',
            'labels': 'Метки',
        }
    def __init__(self, *args, **kwargs):
        initial = kwargs.get('initial', {})
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['status'].choices =[('', '---------')] + [(status.id, status.name) for status in Status.objects.all()]
        self.fields['executor'].choices =[('', '---------')] + [(executor.id, f"{executor.first_name} {executor.last_name}") for executor in
                                           User.objects.all()]
        self.fields['labels'].choices = [(label.id, label.name) for label in Labels.objects.all()]

        self.initial['name'] = initial.get('name', '')
        self.initial['description'] = initial.get('description', '')
        self.initial['status'] = initial.get('status_id', '')
        self.initial['executor'] = initial.get('executor_id', '')
        self.initial['labels'] = initial.get('labels', [])



class TaskFilterForm(forms.Form):
    status = forms.ChoiceField(
        label='Статус',
        label_suffix='',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select '})
    )
    executor = forms.ChoiceField(
        label='Исполнитель',
        label_suffix='',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select '})
    )
    label = forms.ChoiceField(
        label='Метка',
        label_suffix='',
        choices=[],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select '})
    )
    self_tasks = forms.BooleanField(
        label='Только свои задачи',
        label_suffix='',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)

        self.fields['status'].choices = [('', '---------')] + [(status.id, status.name) for status in Status.objects.all()]
        self.fields['executor'].choices = [('', '---------')] + [(u.id, f"{u.first_name} {u.last_name}") for u in User.objects.all()]
        self.fields['label'].choices = [('', '---------')] + [(label.id, label.name) for label in Labels.objects.all()]


