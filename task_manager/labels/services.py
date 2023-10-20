from task_manager.labels.models import Labels
from task_manager.tasks.models import Tasks
def create_label(form):
    label = Labels()
    if form.is_valid():
        label_name = form.cleaned_data['name']
        label.name = label_name
        label.save()
        return True
    return False


def get_label_info(label_id):
    label = Labels.objects.values('name').filter(id=label_id)
    label = list(label)
    return label


def delete_label(label_id):
    label = Labels.objects.get(id=label_id)
    if not Tasks.objects.filter(labels=label):
        label.delete()
        return True
    return False


def get_initial_data(label_id):
    label = Labels.objects.get(id=label_id)
    initial_data = {
        'name': label.name,
    }
    return initial_data

def update_label(form, label_id):
    label = Labels.objects.get(id=label_id)
    if form.is_valid():
        name = form.cleaned_data['name']
        label.name = name
        label.save()
        return True
    return False
