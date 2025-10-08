from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.partners.models import PartnerActivity

@login_required
@require_POST
def read_partner_notifications(request):
    """Прочитать уведомления партнёра"""
    partner = request.user
    if not hasattr(partner,"partner_profile"):
        return redirect('index')
    PartnerActivity.objects.filter(partner=partner.partner_profile,
        is_read=False
    ).update(is_read=True)
    
    return redirect("partner_dashboard")