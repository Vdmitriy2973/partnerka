from django.shortcuts import render,redirect

from .common import _get_available_projects
from partner_app.utils import _paginate

def partner_settings(request):  
    """Настройки партнёра"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    context = {
    }
    
    return render(request, 'partner_app/dashboard/partner/settings/settings.html',context=context)