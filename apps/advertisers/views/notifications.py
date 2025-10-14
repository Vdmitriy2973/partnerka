from django.shortcuts import render,redirect
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.advertisers.models import AdvertiserActivity
from apps.tracking.models import Conversion

def notifications(request):  
    """Уведомления рекламодателя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    unread_notifications_count = AdvertiserActivity.objects.filter(advertiser=user.advertiserprofile,is_read=False).count()
    total_notifications_count = AdvertiserActivity.objects.filter(advertiser=user.advertiserprofile).count()
    today_conversions_count = Conversion.objects.filter(advertiser=user.advertiserprofile, created_at__date=timezone.now()).count()
    
    
    notifications  = AdvertiserActivity.objects.filter(advertiser=user.advertiserprofile).order_by('-created_at')    
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
    
    return render(request, 'advertisers/notifications/notifications.html',context=context)


