from django.shortcuts import render, redirect
from .dashboard_utils import (
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
            if hasattr(user,"advertiserprofile"):
                return redirect('advertiser_settings')
            elif hasattr(user,"partner_profile"):
                return redirect('partner_settings')
            return redirect('dashboard')
        elif "password_submit" in request.POST:
            _handle_password_update(request, user)
            if hasattr(user,"advertiserprofile"):
                return redirect('advertiser_settings')
            elif hasattr(user,"partner_profile"):
                return redirect('partner_settings')
            return redirect('dashboard')
    
    
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    # Обработчики личного кабинета
    handlers = {
        "manager": handle_manager_dashboard,
    }
    if user.user_type == "advertiser":
        return redirect('advertiser_dashboard')
    elif user.user_type == "partner":
        return redirect('partner_dashboard')
    return handlers.get(user.user_type, lambda r: None)(request)