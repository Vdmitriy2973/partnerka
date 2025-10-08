from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.partners.models import PartnerActivity


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """
    Отметить одно уведомление как прочитанное
    """
    partner = request.user.partner_profile
    try:
        notification = PartnerActivity.objects.get(id=notification_id, partner=partner)
        notification.is_read = True
        notification.save()
        return JsonResponse({"success": True, "notification_id": notification_id})
    except PartnerActivity.DoesNotExist:
        return JsonResponse({"success": False, "error": "Уведомление не найдено"}, status=404)