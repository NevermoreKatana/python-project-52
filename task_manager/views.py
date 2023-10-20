from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import rollbar
from task_manager.forms import LoginForm
from task_manager import services

class IndexView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        rollbar.report_exc_info()
        return render(request, 'index.html', {'is_session_active': is_session_active})


class LoginView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        rollbar.report_exc_info()
        form = LoginForm()
        return render(request, 'login.html', {'is_session_active': is_session_active, 'form':form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if services.login_user(form, request):
            return services.handle_success(request, 'Вы залогинены', 'main')
        initial_data = services.initial_login_data(form)
        form = LoginForm(initial_data, is_valid=True)

        messages.info(request, 'Пожалуйста, введите правильные имя пользователя и пароль.'
                               '     Оба поля могут быть чувствительны к регистру.')
        rollbar.report_exc_info()
        return render(request, 'login.html', {'form': form})


class LogoutView(View):

    def post(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Вы разлогинены')
        rollbar.report_exc_info()
        return redirect('main')
