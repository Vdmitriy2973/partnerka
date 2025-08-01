from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from partner_app.forms import PlatformForm
from partner_app.models import Platform

@login_required
@require_POST
def add_platform(request):
    form = PlatformForm(request.POST)
    try:
        exc = None
        platform = form.save(commit=False)
        platform.partner = request.user
        platform.save()
        return redirect("dashboard")
    except Exception as e:
        print(form.errors)
        exc = e 
        if "description" in form.errors:
            messages.error(request, "Описание должно содержать минимум 15 символов.",extra_tags="platform_add_error")
        else:
            messages.error(request, "Уже существует площадка с таким  URL или ID или названием.",extra_tags="platform_add_error")
        
    if not exc: 
        messages.success(request,f"Платформа {platform.name} успешно добавлена",extra_tags="platform_add_success")
    return redirect("dashboard")

@login_required
@require_POST
def edit_platform(request,platform_id):
    """Изменить платформу"""
    platform = Platform.objects.get(id=platform_id,partner=request.user)
    try:
        exc = None
        platform.name = request.POST.get('name', platform.name)
        platform.url_or_id = request.POST.get('url', platform.url_or_id)
        platform.platform_type = request.POST.get('type',platform.platform_type)
        platform.description = request.POST.get('description', platform.description)
        print(request.POST)
        # Валидация
        platform.full_clean()
        platform.save()
    except Exception as e:
        print("error:", e)
        exc = e 
        messages.error(request, "Ошибка редактирования платформы.",extra_tags="platform_edit_error")
    
    if not exc: 
        messages.success(request,f"Платформа {platform.name} успешно отредактирована",extra_tags="platform_edit_success")
    return redirect("dashboard")

@login_required
@require_POST
def delete_platform(request, platform_id):
    try:
        platform = Platform.objects.get(id=platform_id,partner=request.user)
        platform.delete()
        messages.success(request,f"Платформа {platform.name} успешно удалена",extra_tags="platform_delete_success")
    except Exception as e:
        print("error:", e)
        messages.error(request, "Ошибка удаления платформы.",extra_tags="platform_delete_error")
    return redirect("dashboard")


# Для модераторов
@login_required
@require_POST
def approve_platform(request, platform_id):
    platform = Platform.objects.get(id=platform_id)
    platform.status = 'Подтверждено'
    platform.save()
    return redirect("dashboard")


@login_required
@require_POST
def reject_platform(request, platform_id):
    platform = Platform.objects.get(id=platform_id)
    platform.status = 'Отклонено'
    platform.is_active = False
    platform.save()
    return redirect("dashboard")
