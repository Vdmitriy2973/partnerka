from django.shortcuts import render, redirect

from partner_app.models import AdvertiserActivity


def advertiser_requisites(request):
    """Страница с настройками юр. данных рекламодателя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    notifications_count = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile).count()
    
    context = {
        "notifications_count":notifications_count
    }
    
    return render(request, 'partner_app/dashboard/advertiser/requisites/requisites.html',context=context)