from django.shortcuts import redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from partner_app.models import ProjectPartner,Project
from partner_app.utils import send_email_via_mailru

@login_required
@require_POST
def connect_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id)
    except Project.DoesNotExist:
        return redirect('dashboard')
    partner = request.user
    
    if ProjectPartner.objects.filter(project=project, partner=partner).exists():
        messages.warning(request, 'Вы уже подключены к этому проекту',extra_tags="already_connected_project")
        return redirect('dashboard')
        
    
    send_email_via_mailru(project.advertiser.email,f"К проекту {project.name} подключился партнёр {partner.get_full_name()} {partner.email}","Новый партнёр")
    
    ProjectPartner.objects.create(
        project=project,
        partner=partner,
        custom_commission=project.commission_rate,
        advertiser=project.advertiser
    )
    return redirect("dashboard")