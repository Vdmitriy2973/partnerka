from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.utils import IntegrityError

from partner_app.forms import ProjectForm
from partner_app.models import Project, ProjectParam, AdvertiserActivity
from django.contrib import messages

import json
import traceback

@login_required
@require_POST
def add_project(request):
    form = ProjectForm(request.POST)
    print("Incoming POST data:", request.POST)  # Логируем входящие данные
    
    if not form.is_valid():
        print("Form errors:", form.errors.as_json())  # Детальный лог ошибок валидации
        messages.error(request, f"Ошибка валидации: {form.errors.as_text()}", extra_tags="project_add_error")
        return redirect("dashboard")
    
    try:
        project = form.save(commit=False)
        project.advertiser = request.user
        
        # Обработка шаблона ссылки (только если он был предоставлен)
        if project.link_template:
            # Добавляем параметры в правильном порядке
            params = ["pid=partner_id"]  # Начинаем с partner_id
            
            params_data = json.loads(request.POST.get('params_json', '[]'))
            for param in params_data:
                param_name = param.get('name', '')
                param_value = param.get('example', '')
                if param_name:  # Только если имя параметра не пустое
                    params.append(f"{param_name}={param_value}")
            
            # Собираем итоговую ссылку
            separator = '?' if '?' not in project.link_template else '&'
            project.link_template += separator + '&'.join(params)
        
        project.save()  # Сохраняем проект
        
        # Главный параметр ID партнёра
        ProjectParam.objects.create(
            project=project,
            name='pid',
            description='ID партнёра. Укажите ID вашего партнёрского аккаунта',
            param_type='required',
            example_value='111'
        )
        # Создаем параметры (после сохранения проекта, чтобы была связь)
        for param in params_data:
            ProjectParam.objects.create(
                project=project,
                name=param['name'],
                description=param.get('description', ''),
                param_type=param.get('type', 'optional'),
                example_value=param.get('example', '')
            )
        
        messages.success(request, "Проект успешно добавлен", extra_tags="project_add_success")
    
    except IntegrityError as e:
        print("IntegrityError:", str(e))
        messages.error(request, "Уже существует проект с таким URL или названием", extra_tags="project_add_error")
    
    except json.JSONDecodeError as e:
        print("JSONDecodeError:", str(e))
        messages.error(request, "Ошибка в формате параметров", extra_tags="project_add_error")
    
    except Exception as e:
        print("Unexpected error:", str(e))
        traceback.print_exc()  # Печать полного трейсбека
        messages.error(request, f"Произошла непредвиденная ошибка: {str(e)}", extra_tags="project_add_error")
        
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
    AdvertiserActivity.objects.create(
        advertiser=project.advertiser.advertiserprofile,
        activity_type='approve',
        title='Проект одобрен',
        details=f'{project.name} был одобрен модератором'
    )
    return redirect("dashboard")


@login_required
@require_POST
def reject_project(request, project_id):
    project = Project.objects.get(id=project_id)
    project.status = 'Отклонено'
    project.is_active = False
    project.save()
    AdvertiserActivity.objects.create(
        advertiser=project.advertiser.advertiserprofile,
        activity_type='reject',
        title='Проект отклонен',
        details=f'{project.name} был отклонен модератором'
    )
    return redirect("dashboard")
