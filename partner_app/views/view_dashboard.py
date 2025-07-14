from django.shortcuts import render, redirect
from .dashboard_utils import (
    handle_partner_dashboard,
    handle_advertiser_dashboard,
    handle_manager_dashboard
)
from .dashboard_utils.handlers import (
    _handle_password_update,
    _handle_profile_update
)

def dashboard(request):
    """Главный обработчик личного кабинета"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')

    if request.method == "POST":
        if "profile_submit" in request.POST:
            _handle_profile_update(request, user)
        elif "password_submit" in request.POST:
            _handle_password_update(request, user)
    
    # Обработчики личного кабинета
    handlers = {
        "partner": handle_partner_dashboard,
        "advertiser": handle_advertiser_dashboard,
        "manager": handle_manager_dashboard
    }
    
    return handlers.get(user.user_type, lambda r: None)(request)