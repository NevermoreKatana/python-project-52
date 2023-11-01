import rollbar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import reverse
from django.contrib.auth import logout
from django.http import HttpResponseRedirect


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return super().handle_no_permission()


class GetSuccessUrlMixin:
    logout = False


    def get_success_url(self):
        if self.logout:
            logout(self.request)
        messages.success(self.request, self.success_message)
        rollbar.report_exc_info()
        return HttpResponseRedirect(reverse(self.custom_success_url))
