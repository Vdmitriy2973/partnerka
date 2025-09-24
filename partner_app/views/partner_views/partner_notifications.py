from django.shortcuts import render,redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from partner_app.models import PartnerActivity, Conversion

def partner_notifications(request):  
    """Уведомления партнёра"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    unread_notifications_count = PartnerActivity.objects.filter(partner=user.partner_profile,is_read=False).count()
    total_notifications_count = PartnerActivity.objects.filter(partner=user.partner_profile).count()
    today_conversions_count = Conversion.objects.filter(partner=user.partner_profile, created_at__date=timezone.now()).count()
    
    
    notifications  = PartnerActivity.objects.filter(partner=user.partner_profile).order_by('-created_at')    
    notifications_page = Paginator(notifications,10)
    
    page = request.GET.get('page', 1)
    
    try:
        notifications_page = notifications_page.page(page)
    except (PageNotAnInteger, EmptyPage):
        notifications_page = notifications_page.page(1)
    context = {
        "user": request.user,
        
        "notifications":notifications_page,
        "notifications_count":unread_notifications_count,
        "total_notifications_count":total_notifications_count,
        
        "today_conversions_count":today_conversions_count,
    }
    
    return render(request, 'partner_app/dashboard/partner/notifications/notifications.html',context=context)


