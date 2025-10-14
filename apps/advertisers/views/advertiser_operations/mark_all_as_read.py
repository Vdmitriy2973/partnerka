from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from apps.advertisers.models import AdvertiserActivity

@login_required
@require_POST
def mark_all_notifications_read(request):
    """
    Отметить все уведомления пользователя как прочитанные
    """
    advertiser = request.user.advertiserprofile
    AdvertiserActivity.objects.filter(advertiser=advertiser, is_read=False).update(is_read=True)
    return JsonResponse({"success": True})