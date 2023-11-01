import rollbar
from django.contrib import messages
from django.shortcuts import redirect


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
