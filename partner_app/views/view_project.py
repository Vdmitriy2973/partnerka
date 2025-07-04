from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from partner_app.forms import ProjectForm
from partner_app.models import Project
from django.contrib import messages

@login_required
@require_POST
def add_project(request):
    form = ProjectForm(request.POST)
    try:
        project = form.save(commit=False)
        project.advertiser  = request.user
        project.save()
        return redirect("dashboard")
    except Exception as e:
        print(e)
        messages.error(request, "Уже существует проект с таким  URL или ID или названием.",extra_tags="project_add_error")
        project = ProjectForm()
        
    return redirect("dashboard")



@login_required
@require_POST
def delete_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.delete()
    return redirect("dashboard")


# Для модераторов
@login_required
@require_POST
def approve_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.status = 'Подтверждено'
    project.save()
    return redirect("dashboard")


@login_required
@require_POST
def reject_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.status = 'Отклонено'
    project.is_active = False
    project.save()
    return redirect("dashboard")
