from django.contrib.auth.models import User
from task_manager.validator import password_validate
from django.contrib.auth.hashers import make_password


def updation_user(form, user_id):
    if form.is_valid():
        user = User.objects.get(id=user_id)
        name = form.cleaned_data['first_name']
        surname = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if not password_validate(password1, password2):
            pass
        user.first_name = name
        user.last_name = surname
        user.username = username
        hashed_password = make_password(password1)
        user.password = hashed_password
        user.save()
        return True
    return False


def registeration_user(form):
    if form.is_valid():
        name = form.cleaned_data['first_name']
        surname = form.cleaned_data['last_name']
        username = form.cleaned_data['username']
        password1 = form.cleaned_data['password1']
        password2 = form.cleaned_data['password2']
        if not password_validate(password1, password2):
            pass
        user = User.objects.create_user(username=username, password=password1)
        user.first_name = name
        user.last_name = surname
        user.save()
        return True
    return False


def format_user():
    users = User.objects.values('username', 'first_name', 'last_name', 'id', 'date_joined')

    formatted_users = []
    for user in users:
        user['date_joined'] = user['date_joined'].strftime('%d.%m.%Y %H:%M')
        formatted_users.append(user)
    return formatted_users


def get_user_info(user_id):
    user = User.objects.values('first_name', 'last_name').filter(id=user_id)
    user = list(user)
    return user[0] if user else None


def get_update_user_info(user_id):
    user = User.objects.values('first_name', 'last_name', 'username').filter(id=user_id)
    user = list(user)
    return initial_user_data(user[0])


def is_session_active(request, user_id):
    return request.session.get('user_id') is user_id


def check_user(model, user):
    if model.objects.filter(executor=user) or model.objects.filter(author=user):
        return False
    return True


def initial_user_data(user_data):
    initial_data = {
        'first_name': user_data['first_name'],
        'last_name': user_data['last_name'],
        'username': user_data['username'],
    }
    return initial_data

