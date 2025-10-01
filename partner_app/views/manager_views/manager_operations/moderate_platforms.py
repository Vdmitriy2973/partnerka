from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages


from partner_app.models import Platform, PartnerActivity
from utils import send_email_via_mailru

@login_required
@require_POST
def approve_platform(request, platform_id):
    platform = get_object_or_404(Platform,id=platform_id)
    platform.status = 'Подтверждено'
    platform.save()
    if platform.partner.email_notifications:
        try:
            send_email_via_mailru.delay(platform.partner.email,f"Платформа {platform.name} была одобрена модератором", 'Уведомление о подтверждении платформы')
        except:
            pass
    PartnerActivity.objects.create(
        partner=platform.partner.partner_profile,
        activity_type='approve',
        title='Платформа одобрена',
        details=f'{platform.name} была одобрена модератором'
    )
    messages.success(request,message=f"Платформа {platform.name} была одобрена",extra_tags="approve_success")
    return redirect("manager_platforms")

@login_required
@require_POST
def reject_platform(request, platform_id):
    platform = get_object_or_404(Platform,id=platform_id)
    platform.status = 'Отклонено'
    platform.is_active = False
    platform.save()
    reason = request.POST.get('moderation_rejection_reason')
    if platform.partner.email_notifications:
        try:
            send_email_via_mailru.delay(platform.partner.email,f"Платформа {platform.name} была отклонена модератором по причине: {reason}", 'Уведомление об отклонении платформы')
        except:
            pass
    PartnerActivity.objects.create(
        partner=platform.partner.partner_profile,
        activity_type='reject',
        title='Платформа отклонена',
        details=f'{platform.name} была отклонена модератором. Причина: {reason}'
    )
    messages.success(request,message=f"Платформа {platform.name} была отклонена",extra_tags="reject_success")
    return redirect("manager_platforms")
