from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def advertiser_partners(request):
    return render(request, 'partner_app/dashboard/advertiser/partners.html')