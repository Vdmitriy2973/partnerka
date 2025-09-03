from django.shortcuts import render

from partner_app.forms import PartnerRegistrationForm, AdvertiserRegistrationForm, LoginForm

from .index_utils.auth import handle_login
from .index_utils.reg import handle_registration


def index(request):
    if request.method == "POST":
        if "reg_type" in request.POST:
            reg_type = request.POST["reg_type"]
            response = handle_registration(request, reg_type)
            if response:
                return response
        elif "auth" in request.POST:
            response = handle_login(request)
            if response:
                return response

    return render(request, "partner_app/main/index.html", {
        'partner_form': PartnerRegistrationForm(),
        'advertiser_form': AdvertiserRegistrationForm(),
        'login_form': LoginForm()
    })