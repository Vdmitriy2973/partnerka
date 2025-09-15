from django.shortcuts import render,redirect
from django.conf import settings

from partner_app.models import User, Conversion,Project,AdvertiserActivity

def advertiser_dashboard(request):  
    """Информационная панель рекламодателя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    partners = User.objects.filter(
        project_memberships__project__advertiser=request.user
    ).distinct().count()
    projects = Project.objects.filter(
        advertiser=request.user
    ).filter(status='Подтверждено').count()
    conversions = Conversion.objects.filter(advertiser=request.user.advertiserprofile).count()
    last_activity = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile).order_by('-created_at')[:5]
    
    notifications_count = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile).count()
    
    context = {
        "user": request.user,
        "partners_count": partners,
        "user_projects_count": projects,
        "conversions_count":conversions,
        
        "last_activity":last_activity,
        "notifications_count":notifications_count,
        "min_payout": settings.PARTNER_PAYOUT_SETTINGS["min_amount"],
        "fee_percent": settings.PARTNER_PAYOUT_SETTINGS["fee_percent"],
        
    }
    return render(request, 'partner_app/dashboard/advertiser/dashboard/dashboard.html',context=context)