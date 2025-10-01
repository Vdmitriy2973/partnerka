from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.http import require_POST

from apps.core.forms import LoginForm


@require_POST
def handle_login(request):
    """обработчик авторизации"""
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            request.session.set_expiry(1209600)
        else:
            request.session.set_expiry(0)
        login(request, user)
        return redirect("dashboard")
    else:
        messages.error(request, message="Неверный email или пароль.",extra_tags="login_error")
    return redirect('/?show_modal=auth')