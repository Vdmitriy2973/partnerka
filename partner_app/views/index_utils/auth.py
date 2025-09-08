from django.shortcuts import redirect
from django.contrib.auth import login
from django.contrib import messages
from partner_app.forms import LoginForm

def handle_login(request):
    form = LoginForm(request, data=request.POST)
    if form.is_valid():
        user = form.get_user()
        remember_me = form.cleaned_data.get("remember_me")
        if remember_me:
            request.session.set_expiry(1209600)
        else:
            request.session.set_expiry(0)
        login(request, user)
        if hasattr(request.user,"advertiserprofile"):
            return redirect("advertiser_dashboard")
        elif hasattr(request.user,"partner_profile"):
            return redirect("partner_dashboard")
        return redirect("dashboard")
    else:
        messages.error(request, message="Неверный email или пароль.",extra_tags="login_error")
    return redirect('/?show_modal=auth')
