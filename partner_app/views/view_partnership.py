from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_POST
from partner_app.models import ProjectPartner

@login_required
@require_POST
@transaction.atomic
def stop_partnership_with_project(request,project_id):
    """Остановить сотрудничество партнёра с проектом рекламодателя"""
    partnership = ProjectPartner.objects.get(partner=request.user,project=project_id)
    partnership.delete()
    return redirect('dashboard')


@login_required
@require_POST
@transaction.atomic
def stop_partnership_with_partner(request,partner_id):
    """Остановить сотрудничество рекламодателя с партнёром"""
    
    partnership = ProjectPartner.objects.filter(
        advertiser=request.user,
        partner=partner_id
    )
    partnership.delete()
    return redirect('dashboard')

@login_required
@require_POST
def suspend_partnership(request,project_id):
    """Приостановить сотрудничество партнёра с проектом рекламодателя"""
    partnership = ProjectPartner.objects.get(partner=request.user,project=project_id)
    partnership.status = "Приостановлен"
    partnership.save()
    return redirect('dashboard')


@login_required
@require_POST
def resume_partnership(request,project_id):
    """ Воозобновить сотрудничество партнёра с проектом рекламодателя"""
    partnership = ProjectPartner.objects.get(partner=request.user,project=project_id)
    partnership.status = "Активен"
    partnership.save()
    return redirect('dashboard')