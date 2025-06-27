# partner_app/views/dashboard.py

from django.shortcuts import render, redirect

from .dashboard_utils.handlers import _handle_password_update,_handle_profile_update,_get_dashboard_template
from partner_app.forms import PlatformForm
from partner_app.models import Platform

def dashboard(request):
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')

    if request.method == "POST":
        if "profile_submit" in request.POST:
            _handle_profile_update(request, user)
        elif "password_submit" in request.POST:
            _handle_password_update(request, user)

    template = _get_dashboard_template(user.user_type)
    if not template:
        return render(request, "errors/403.html")
    
    
    if user.user_type == "partner":
        platforms = Platform.objects.filter(partner=request.user).order_by('-created_at')
        context = {
            "user":user,
            'platformForm': PlatformForm(),
            'platforms': platforms,
            'total_platforms': platforms.count(),
            'approved_platforms': platforms.filter(status='Подтверждено').count(),
            'pending_platforms': platforms.filter(status='На модерации').count(),
        }
        return render(request, template, context)
    else:
        return render(request, template, {"user":user})


