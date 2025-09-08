from django.shortcuts import render, redirect
from partner_app.forms import ApiSettingsForm

def advertiser_settings(request):
    """Настройки рекламодателя"""
    
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    
    context = {
        "apiSettingsForm": ApiSettingsForm(request=request)
    }
    return render(request, 'partner_app/dashboard/advertiser/settings/settings.html',context=context)