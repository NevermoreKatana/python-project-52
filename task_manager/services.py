import rollbar
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout


def handle_error(request, message, redirect_url, report_exception=True):
    if report_exception:
        rollbar.report_exc_info()
    messages.error(request, message)
    return redirect(redirect_url)


def handle_success(request, message, redirect_url, report_exception=True):
    if report_exception:
        rollbar.report_exc_info()
    messages.success(request, message)
    return redirect(redirect_url)

def handle_info(request, message, redirect_url, report_exception=True):
    if report_exception:
        rollbar.report_exc_info()
    messages.info(request, message)
    return redirect(redirect_url)


def login_user(form, request):
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['user_id'] = user.id
            request.session['username'] = user.username
            return True
        return False


def initial_login_data(form):
    initial_data = {
        'username': form.cleaned_data['username'],
    }
    return initial_data
