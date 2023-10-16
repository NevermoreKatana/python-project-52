from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import rollbar


class IndexView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        rollbar.report_exc_info()
        return render(request, 'index.html', {'is_session_active': is_session_active})


class LoginView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        rollbar.report_exc_info()
        return render(request, 'login.html', {'is_session_active': is_session_active})

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            messages.success(request, 'Вы залогинены')
            rollbar.report_exc_info()
            return redirect('main')
        messages.info(request, 'Пожалуйста, введите правильные имя пользователя и пароль. Оба поля могут быть чувствительны к регистру.')
        rollbar.report_exc_info()
        return render(request, 'login.html', {'username': username})


class LogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        rollbar.report_exc_info()
        return redirect('main')
