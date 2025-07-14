from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from partner_app.models import ProjectPartner

@login_required
@require_POST
def stop_partnership(request,project_id):
    """Остановить сотрудничество партнёра с проектом рекламодателя"""
    partnership = ProjectPartner.objects.get(partner=request.user,project=project_id)
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