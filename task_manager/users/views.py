from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout
from task_manager.validator import password_validate
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from task_manager.tasks.models import Tasks
import rollbar


class UserView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        users = User.objects.values('username', 'first_name', 'last_name', 'id', 'date_joined')

        formatted_users = []
        for user in users:

            user['date_joined'] = user['date_joined'].strftime('%d.%m.%Y %H:%M')
            formatted_users.append(user)
        rollbar.report_exc_info()
        return render(request, 'users/index.html', {'users': formatted_users, 'is_session_active': is_session_active})


class UserCreateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        rollbar.report_exc_info()
        return render(request, 'users/create.html', {'is_session_active': is_session_active})

    def post(self, request, *args, **kwargs):
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password_validate(password1, password2):
            user = User.objects.create_user(username=username, password=password1)
            user.save()

            user.first_name = name
            user.last_name = surname
            user.save()
            rollbar.report_exc_info()
            return redirect('login')


class UserDeleteView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if request.session.get('user_id') is user_id:
            user = User.objects.values('first_name', 'last_name').filter(id=user_id)
            user = list(user)
            rollbar.report_exc_info()
            return render(request, 'users/delete.html', {'is_session_active': is_session_active, 'user': user[0]})
        elif not is_session_active:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            rollbar.report_exc_info()
            return redirect('login')
        messages.error(request, 'У вас нет прав для изменения другого пользователя.')
        rollbar.report_exc_info()
        return redirect('users_index')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        if Tasks.objects.filter(executor=user) or Tasks.objects.filter(author=user):
            messages.error(request, 'Невозможно удалить пользователя, потому что он используется')
            rollbar.report_exc_info()
            return redirect('users_index')
        user.delete()
        messages.success(request, 'Пользователь успешно удален')
        logout(request)
        rollbar.report_exc_info()
        return redirect('users_index')


class UserUpdateView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if request.session.get('user_id') is user_id:
            user = User.objects.values('first_name', 'last_name', 'username').filter(id=user_id)
            user = list(user)
            messages.success(request, 'Пользователь успешно изменен')
            rollbar.report_exc_info()
            return render(request, 'users/update.html', {'is_session_active': is_session_active, 'user': user[0]})
        elif not is_session_active:
            messages.error(request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
            rollbar.report_exc_info()
            return redirect('login')
        messages.error(request, 'У вас нет прав для изменения другого пользователя.')
        rollbar.report_exc_info()
        return redirect('users_index')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        name = request.POST.get('first_name')
        surname = request.POST.get('last_name')
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password_validate(password1, password2):
            user.first_name = name
            user.last_name = surname
            user.username = username
            hashed_password = make_password(password1)
            user.password = hashed_password
            user.save()
            logout(request)
            rollbar.report_exc_info()
            return redirect('users_index')
