from django.shortcuts import render,redirect
from django.conf import settings

from partner_app.models import PartnerActivity
from .common import _get_available_projects,_get_connected_projects

def partner_dashboard(request):  
    """Информационная панель партнёра"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    
    last_activity = PartnerActivity.objects.filter(partner=request.user.partner_profile).order_by('-created_at')[:5]
    available_projects = _get_available_projects(request)     
    connected_projects = _get_connected_projects(request)  
    active_connected_projects = connected_projects.filter(
        partner_memberships__status="Активен"
    ).count()
    clicks_count = request.user.partner_profile.clicks.count() 
    if clicks_count == 0:
        conversion = 0
    else:
        conversion =  f"{(request.user.partner_profile.conversions.count() / request.user.partner_profile.clicks.count()) * 100:.2f}"
    total_projects = available_projects.count()
    
    context = {
        "user": request.user,  
        "int_balance":int(request.user.partner_profile.balance),
        "last_activity":last_activity,
        
        "total_projects":total_projects,
        "active_connected_projects": active_connected_projects,
        "clicks_count":clicks_count,
        "conversion":conversion,
        
        "is_payout_available": request.user.partner_profile.balance > float(settings.PARTNER_PAYOUT_SETTINGS["min_amount"]),
        "min_payout": settings.PARTNER_PAYOUT_SETTINGS["min_amount"],
        "fee_percent": settings.PARTNER_PAYOUT_SETTINGS["fee_percent"],
    }
    
    return render(request, 'partner_app/dashboard/partner/dashboard/dashboard.html',context=context)


