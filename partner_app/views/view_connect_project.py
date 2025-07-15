from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from partner_app.models import ProjectPartner,Project

@login_required
@require_POST
def connect_project(request, project_id):
    # Подключение
    project = get_object_or_404(Project, id=project_id)
    partner = request.user
        
    # Проверяем, не существует ли уже такой связи
    if ProjectPartner.objects.filter(project=project, partner=partner).exists():
        messages.warning(request, 'Вы уже подключены к этому проекту',extra_tags="already_connected_project")
        return redirect('dashboard')
        
    # Создаем новую связь
    ProjectPartner.objects.create(
        project=project,
        partner=partner,
        custom_commission=project.commission_rate,
        advertiser=project.advertiser
    )
    return redirect("dashboard")