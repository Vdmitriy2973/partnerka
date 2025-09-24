from django.shortcuts import render,redirect

from partner_app.models import PartnerActivity

def partner_settings(request):  
    """Настройки партнёра"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    notifications_count = PartnerActivity.objects.filter(partner=request.user.partner_profile,is_read=False).count()
    
    context = {
        'notifications_count':notifications_count
    }
    
    return render(request, 'partner_app/dashboard/partner/settings/settings.html',context=context)