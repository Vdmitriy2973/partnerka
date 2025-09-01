from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def advertiser_dashboard(request):
    return render(request, 'partner_app/dashboard/advertiser/dashboard.html')