from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from partner_app.models import PartnerActivity

@login_required
@require_POST
def mark_all_notifications_read(request):
    """
    Отметить все уведомления пользователя как прочитанные
    """
    partner = request.user.partner_profile
    PartnerActivity.objects.filter(partner=partner, is_read=False).update(is_read=True)
    return JsonResponse({"success": True})