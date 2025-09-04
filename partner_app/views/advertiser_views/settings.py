from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from partner_app.forms import ApiSettingsForm
@login_required
def advertiser_settings(request):
    
    context = {
        "apiSettingsForm": ApiSettingsForm(request=request)
    }
    return render(request, 'partner_app/dashboard/advertiser/settings/settings.html',context=context)