from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings

from partner_app.models import User, Conversion,Project,AdvertiserActivity


@login_required
def advertiser_dashboard(request):
    """Информационная панель рекламодателя"""
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    partners = User.objects.filter(
        project_memberships__project__advertiser=request.user
    ).distinct().count()
    projects = Project.objects.filter(
        advertiser=request.user
    ).filter(status='Подтверждено').count()
    conversions = Conversion.objects.filter(advertiser=request.user.advertiserprofile).count()
    last_activity = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile).order_by('-created_at')[:5]
    context = {
        "user": request.user,
        "partners_count": partners,
        "user_projects_count": projects,
        "conversions_count":conversions,
        
        "last_activity":last_activity,
        "min_payout": settings.PARTNER_PAYOUT_SETTINGS["min_amount"],
        "fee_percent": settings.PARTNER_PAYOUT_SETTINGS["fee_percent"],
        
    }
    return render(request, 'partner_app/dashboard/new_advertiser/dashboard/dashboard.html',context=context)