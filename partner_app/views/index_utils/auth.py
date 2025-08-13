from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from partner_app.utils import send_email_via_mailru
from partner_app.forms import LoginForm

def handle_login(request):
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            print("remembered")
            request.session.set_expiry(1209600)
        login(request, user)
        send_email_via_mailru(user.email,"Произошла авторизация с нового устройства","🔒 Обнаружен вход в ваш аккаунт с нового устройства")
        return redirect("dashboard")
    else:
        messages.error(request, "Неверный email или пароль.",extra_tags="login_error")
    return redirect('/?show_modal=auth')
