from django.shortcuts import render, redirect

from apps.advertisers.models import AdvertiserActivity


def requisites(request):
    """Страница с настройками юр. данных рекламодателя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    notifications_count = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile,is_read=False).count()
    
    context = {
        "notifications_count":notifications_count
    }
    
    return render(request, 'advertisers/requisites/requisites.html',context=context)