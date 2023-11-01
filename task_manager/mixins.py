import rollbar
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = 'login'

    def handle_no_permission(self):
        messages.error(self.request, 'Вы не авторизованы! Пожалуйста, выполните вход.')
        rollbar.report_exc_info()
        return super().handle_no_permission()
