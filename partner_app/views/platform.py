from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from partner_app.forms import PlatformForm
from partner_app.models import Platform, PartnerActivity
from partner_app.utils import send_email_via_mailru

@login_required
@require_POST
def add_platform(request):
    form = PlatformForm(request.POST)
    try:
        platform = form.save(commit=False)
        platform.partner = request.user
        platform.save()
        messages.success(request,message=f"Платформа {platform.name} успешно добавлена",extra_tags="platform_add_success")
        return redirect("partner_platforms")
    except Exception as e:
        if "description" in form.errors:
            messages.error(request, message="Описание должно содержать минимум 15 символов.",extra_tags="platform_add_error")
        else:
            messages.error(request, message="Уже существует площадка с таким  URL или названием.",extra_tags="platform_add_error")
    return redirect("partner_platforms")

@login_required
@require_POST
def edit_platform(request,platform_id):
    """Изменить платформу"""
    platform = get_object_or_404(Platform,id=platform_id,partner=request.user)
    try:
        platform.name = request.POST.get('name', platform.name)
        platform.url_or_id = request.POST.get('url', platform.url_or_id)
        platform.platform_type = request.POST.get('type',platform.platform_type)
        platform.description = request.POST.get('description', platform.description)
        if request.POST.get('is_active',None):
            platform.is_active = True
        else:
            platform.is_active = False
        # Валидация
        platform.full_clean()
        platform.save()
        messages.success(request,message=f"Платформа {platform.name} успешно отредактирована",extra_tags="platform_edit_success")
        return redirect("partner_platforms")
    except Exception as e:
        for num,(field,error) in enumerate(e.message_dict.items()):
            messages.error(request, f"{num+1}. {field} : {error[0]}",extra_tags="platform_edit_error")
    return redirect("partner_platforms")

@login_required
@require_POST
def delete_platform(request, platform_id):
    try:
        platform = get_object_or_404(Platform,id=platform_id,partner=request.user)
        platform.delete()
        messages.success(request,message=f"Платформа {platform.name} успешно удалена",extra_tags="platform_delete_success")
    except Exception as e:
        messages.error(request, message=f"Ошибка удаления платформы: {e}",extra_tags="platform_delete_error")
    return redirect("partner_platforms")


# Для модераторов
@login_required
@require_POST
def approve_platform(request, platform_id):
    platform = get_object_or_404(Platform,id=platform_id)
    platform.status = 'Подтверждено'
    platform.save()
    send_email_via_mailru.delay(platform.partner.email,f"Платформа {platform.name} была одобрена модератором", 'Уведомление о подтверждении платформы')
    PartnerActivity.objects.create(
        partner=platform.partner.partner_profile,
        activity_type='approve',
        title='Платформа одобрена',
        details=f'{platform.name} была одобрена модератором'
    )
    messages.success(request,message=f"Платформа {platform.name} была одобрена",extra_tags="approve_success")
    return redirect("dashboard")

@login_required
@require_POST
def reject_platform(request, platform_id):
    platform = get_object_or_404(Platform,id=platform_id)
    platform.status = 'Отклонено'
    platform.is_active = False
    platform.save()
    reason = request.POST.get('moderation_rejection_reason')
    send_email_via_mailru.delay(platform.partner.email,f"Платформа {platform.name} была отклонена модератором по причине: {reason}", 'Уведомление об отклонении платформы')
    PartnerActivity.objects.create(
        partner=platform.partner.partner_profile,
        activity_type='reject',
        title='Платформа отклонена',
        details=f'{platform.name} была отклонена модератором. Причина: {reason}'
    )
    messages.success(request,message=f"Платформа {platform.name} была отклонена",extra_tags="reject_success")
    return redirect("dashboard")
