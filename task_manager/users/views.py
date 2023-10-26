from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import logout
from task_manager.tasks.models import Tasks
import rollbar
from task_manager.users.forms import RegistrationForm
from task_manager.users import services
from task_manager.services import handle_success, handle_error
from django.views.generic import ListView


class UserView(ListView):
    model = User
    template_name = 'users/index.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context


class UserCreateView(View):

    def get(self, request, *args, **kwargs):
        is_session_active = 'user_id' in request.session
        rollbar.report_exc_info()
        form = RegistrationForm
        return render(request, 'users/create.html',
                      {'is_session_active': is_session_active,
                       'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if services.registeration_user(form):
            return handle_success(request, 'Пользователь успешно зарегистрирован', 'login')


class UserDeleteView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        session_active = 'user_id' in request.session
        if services.is_session_active(request, user_id):
            user = services.get_user_info(user_id)
            return render(request, 'users/delete.html', {'is_session_active': True, 'user': user})
        elif not session_active:
            return handle_error(request,
                                'Вы не авторизованы! Пожалуйста, выполните вход.',
                                'login')
        return handle_error(request,
                            'У вас нет прав для изменения другого пользователя.',
                            'users_index')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        user = User.objects.get(id=user_id)
        if not services.check_user(Tasks, user):
            return handle_error(request,
                                'Невозможно удалить пользователя, потому что он используется',
                                'users_index')
        user.delete()
        logout(request)
        return handle_success(request,
                              'Пользователь успешно удален',
                              'users_index')


class UserUpdateView(View):

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        is_session_active = 'user_id' in request.session
        if services.is_session_active(request, user_id):
            user = services.get_update_user_info(user_id)
            form = RegistrationForm(user)
            rollbar.report_exc_info()
            return render(request, 'users/update.html',
                          {'is_session_active': is_session_active,
                           'form': form})
        elif not is_session_active:
            return handle_error(request,
                                'Вы не авторизованы! Пожалуйста, выполните вход.',
                                'login')
        return handle_error(request,
                            'У вас нет прав для изменения другого пользователя.',
                            'users_index')

    def post(self, request, *args, **kwargs):
        user_id = kwargs.get('pk')
        form = RegistrationForm(request.POST)
        if services.updation_user(form, user_id):
            logout(request)
            return handle_success(request, 'Пользователь успешно изменен', 'users_index')
