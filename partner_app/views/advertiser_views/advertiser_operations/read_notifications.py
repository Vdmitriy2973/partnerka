from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from partner_app.models import AdvertiserActivity

@login_required
@require_POST
def read_advertiser_notifications(request):
    """Прочитать уведомления рекламодателя"""
    advertiser = request.user
    if not hasattr(advertiser,"advertiserprofile"):
        return redirect('index')
    AdvertiserActivity.objects.filter(advertiser=advertiser.advertiserprofile).delete()
   
    return redirect("advertiser_dashboard")