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
        messages.success(request, "Проект успешно добавлен",extra_tags="project_add_success")
    except Exception as e:
        print(e)
        messages.error(request, "Уже существует проект с таким  URL или ID или названием",extra_tags="project_add_error")
        
    return redirect("dashboard")



@login_required
@require_POST
def delete_project(request, project_id):
    try:
        project = Project.objects.get(id=project_id,advertiser=request.user)
        project.delete()
        messages.success(request, "Проект успешно удалён",extra_tags="project_delete_success")
    except Exception as e:
        print(e)
        messages.success(request, "Произошла ошибка при удалении проекта",extra_tags="project_delete_error")
    return redirect("dashboard")


@login_required
@require_POST
def edit_project(request,project_id):
    project = Project.objects.get(id=project_id,advertiser=request.user)
    try:
        exc = None
        project.name = request.POST.get('name', project.name)
        project.url = request.POST.get('url', project.url)
        project.description = request.POST.get('description', project.description)
        project.cookie_lifetime = int(request.POST.get('cookie_lifetime', project.cookie_lifetime))
        project.commission_rate = int(request.POST.get('commission_rate', project.commission_rate))
        project.min_payout = float(request.POST.get('min_payout', project.min_payout))
        if request.POST.get('is_active',None):
            project.is_active = True
        else:
            project.is_active = False
        
        # Валидация
        project.full_clean()
        project.save()
    except Exception as e:
        print("error:", e)
        exc = e
        messages.error(request, "Ошибка редактирования проекта",extra_tags="project_edit_error")
    
    if not exc:
        messages.success(request,f"Проект {project.name} успешно отредактирован",extra_tags="project_edit_success")
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
