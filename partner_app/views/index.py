from django.shortcuts import render

from partner_app.forms import PartnerRegistrationForm, AdvertiserRegistrationForm, LoginForm
def index(request):
    return render(request, "partner_app/main/index.html", {
        'partner_form': PartnerRegistrationForm(),
        'advertiser_form': AdvertiserRegistrationForm(),
        'login_form': LoginForm()
    })