from django.shortcuts import render

from apps.core.forms import PartnerRegistrationForm, AdvertiserRegistrationForm, LoginForm
def index(request):
    return render(request, "core/main/index.html", {
        'partner_form': PartnerRegistrationForm(),
        'advertiser_form': AdvertiserRegistrationForm(),
        'login_form': LoginForm()
    })