import rollbar
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login


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