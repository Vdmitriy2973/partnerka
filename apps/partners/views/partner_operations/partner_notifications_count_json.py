from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET

from apps.partners.models import PartnerActivity


@login_required
@require_GET
def partner_notifications_count_json(request):
    partner = request.user.partner_profile

    qs = PartnerActivity.objects.filter(partner=partner).order_by('-created_at')

    return JsonResponse({
        "notifications_count": qs.count(),
    })
