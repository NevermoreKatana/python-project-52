import rollbar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import reverse
from django.contrib.auth import logout


class CustomLoginRequiredMixin(LoginRequiredMixin):
    '''
    Миксин проверяет, авторизован пользователь или нет, если пользователь не авторизован
    и действие которое он пытается выполнить предназначено только для авторизованных юзеров
    его автоматически редиректит на страницу login_url = str() с сообщением
    '''
    login_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return super().handle_no_permission()


class GetSuccessUrlMixin:
    '''
    Миксин редиректит пользователя на нужный url(success_url), если действия пользователя
    прошли успешно, т.е. пост удалился или обновился и т.д.
    На вход миксин получет success_url = str() - страница редиректа при успехе
    Так же значение logout = bool, по умолчанию False, если после успешного действия пользователя
    сессия должна сброситься, т.е. пользователь должен автоматически выйти, то нужно поставить
    logout = True в классе наследнике.
    '''
    logout = False

    def get_success_url(self):
        if self.logout:
            logout(self.request)
        messages.success(self.request, self.success_message)
        rollbar.report_exc_info()
        return reverse(self.success_url)


class GetContextDataMixin:
    '''
    Микисн возвращает True/False взависимости от того авторизован пользователь или  нет,
    т.е. если пользователь авторизован вернется True - сессия активна, в противном случае - False.
    Эти данные передаются в context Django, что передается в html страницы
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_session_active'] = 'user_id' in self.request.session
        return context
