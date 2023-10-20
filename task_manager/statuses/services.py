from task_manager.statuses.models import Status


def create_status(form):
    status = Status()
    if form.is_valid():
        post_name = form.cleaned_data['name']
        status.name = post_name
        status.save()
        return True
    return False

def update_status(status_id, form):
    status = Status.objects.get(id=status_id)
    if form.is_valid():
        post_name = form.cleaned_data['name']
        status.name = post_name
        status.save()
        return True
    return False


def get_initial_data(status_id):
    status = Status.objects.get(id=status_id)
    initial_data = {
        'name': status.name,
    }
    return initial_data


def delete_status(status_id):
    status = Status.objects.get(id=status_id)
    status.delete()
    return True