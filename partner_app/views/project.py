import json
from decimal import Decimal

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.utils import IntegrityError
from django.contrib import messages

from partner_app.forms import ProjectForm
from partner_app.models import Project, ProjectParam, AdvertiserActivity
from partner_app.utils import send_email_via_mailru


@login_required
@require_POST
def add_project(request):
    form = ProjectForm(request.POST)
    
    if not form.is_valid():
        # Собираем все ошибки в чистый текст
        error_messages = []
        for field, errors in form.errors.items():
            for error in errors:
                # Убираем HTML теги и лишние символы
                clean_error = str(error).replace('<strong>', '').replace('</strong>', '').strip()
                error_messages.append(clean_error)
        
        # Объединяем все ошибки в одну строку
        full_error_message = ". ".join(error_messages)
        messages.error(request, f"Ошибка: {full_error_message}", extra_tags="project_add_error")
        
        return redirect("dashboard")
    
    try:
        project = form.save(commit=False)
        project.advertiser = request.user
        project.first_price = project.cost_per_action
        
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
        
        messages.success(request, message="Проект успешно добавлен", extra_tags="project_add_success")
    
    except IntegrityError as e:
        messages.error(request, message="Уже существует проект с таким URL или названием", extra_tags="project_add_error")
    
    except json.JSONDecodeError as e:
        messages.error(request, message="Ошибка в формате параметров", extra_tags="project_add_error")
    
    except Exception as e:
        for error in e.messages:
            messages.error(request, message=f"Произошла непредвиденная ошибка: {str(error)}", extra_tags="project_add_error")
        
    return redirect("dashboard")



@login_required
@require_POST
def delete_project(request, project_id):
    try:
        project = get_object_or_404(Project,id=project_id,advertiser=request.user)
        project.delete()
        messages.success(request, message="Проект успешно удалён",extra_tags="project_delete_success")
    except Exception as e:
        messages.error(request, message=f"Произошла ошибка при удалении проекта: {e}",extra_tags="project_delete_error")
    return redirect("dashboard")


@login_required
@require_POST   
def edit_project(request,project_id):
    project = get_object_or_404(Project,id=project_id,advertiser=request.user)
    try:
        project.name = request.POST.get('name', project.name)
        project.url = request.POST.get('url', project.url)
        project.description = request.POST.get('description', project.description)
        
        new_price = Decimal(request.POST.get('costPerAction',project.cost_per_action))
        if project.cost_per_action != new_price:
            project.new_cost_per_action = new_price
            project.status = project.StatusType.PENDING
            messages.success(request,message=f"Проект {project.name} отправлен на модерацию из-за изменения цены",extra_tags="project_edit_success")
        if request.POST.get('is_active',None):
            project.is_active = True
        else:
            project.is_active = False
        
        project.save()
    except Exception as e:
        for error in e.messages:
            messages.error(request, f"Ошибка редактирования проекта: {str(error)}",extra_tags="project_edit_error")
        return redirect("dashboard")
    
    
    messages.success(request,message=f"Проект {project.name} успешно отредактирован",extra_tags="project_edit_success")
    return redirect("dashboard")


# Для модераторов
@login_required
@require_POST
def approve_project(request, project_id):
    project = get_object_or_404(Project,id=project_id)
    project.status = 'Подтверждено'
    if project.new_cost_per_action and project.new_cost_per_action != project.cost_per_action:
        project.cost_per_action = project.new_cost_per_action
    project.save()
    send_email_via_mailru.delay(project.advertiser.email,f"Поздравляем, проект {project.name} был одобрен модератором.",'Уведомление о подтвеждении проекта')
    
    AdvertiserActivity.objects.create(
        advertiser=project.advertiser.advertiserprofile,
        activity_type='approve',
        title='Проект одобрен',
        details=f'{project.name} был одобрен модератором'
    )
    messages.success(request,message=f"Проект {project.name} был одобрен",extra_tags="approve_success")
    return redirect("dashboard")


@login_required
@require_POST
def reject_project(request, project_id):
    project = get_object_or_404(Project,id=project_id)
    project.status = 'Отклонено'
    project.is_active = False
    project.save()
    reason = request.POST.get('moderation_rejection_reason')
    send_email_via_mailru.delay(project.advertiser.email,f"Проект {project.name} был отклонен модератором по причине: {reason}", 'Уведомление об отклонении проекта')
    
    AdvertiserActivity.objects.create(
        advertiser=project.advertiser.advertiserprofile,
        activity_type='reject',
        title='Проект отклонен',
        details=f'{project.name} был отклонен модератором. Причина: {reason}'
    )
    messages.success(request,message=f"Проект {project.name} был отклонен",extra_tags="reject_success")
    return redirect("dashboard")
