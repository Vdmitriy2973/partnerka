from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

from .dashboard_utils.handlers import _handle_password_update,_handle_profile_update,_get_dashboard_template

from partner_app.forms import PlatformForm,ProjectForm,ApiSettingsForm
from partner_app.models import Platform,Project



def dashboard(request):
    """Личный кабинет"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')

    if request.method == "POST":
        if "profile_submit" in request.POST:
            _handle_profile_update(request, user)
        elif "password_submit" in request.POST:
            _handle_password_update(request, user)

    template = _get_dashboard_template(user.user_type)
    if not template:
        return render(request, "errors/403.html")
    
    
    if user.user_type == "partner":
        # Основной QuerySet с фильтрацией по пользователю
        user_platforms = Platform.objects.filter(partner=request.user).order_by('-created_at')
        projects = Project.objects.filter(status='Подтверждено').order_by('-created_at')

        # Подсчет статусов ДО пагинации
        total_platforms = user_platforms.count()
        approved_platforms = user_platforms.filter(status='Подтверждено').count()
        pending_platforms = user_platforms.filter(status='На модерации').count()
        
        # пагинатор для платформ
        count = 5
        platform_paginator = Paginator(user_platforms, count)
        platform_page_number = request.GET.get('page')
        platform_page_obj = platform_paginator.get_page(platform_page_number)
        
        # пагинатор для проектов
        count = 6
        project_paginator = Paginator(projects, count)
        project_page_number = request.GET.get('page')
        project_page_obj = project_paginator.get_page(project_page_number)

        context = {
            "user": request.user,  
            'platformForm': PlatformForm(),
            'platforms': platform_page_obj,
            'total_platforms': total_platforms,
            'projects': project_page_obj,
            'total_projects':projects.count(),
            'approved_platforms': approved_platforms,
            'pending_platforms': pending_platforms,
        }
        return render(request, template, context)
    elif user.user_type == "advertiser":

        user_projects = Project.objects.filter(advertiser=request.user).order_by('-created_at')

        total_projects = user_projects.count()
        approved_projects = user_projects.filter(status='Подтверждено').count()
        pending_projects = user_projects.filter(status='На модерации').count()
        
        # Создаем пагинатор
        count = 6
        project_paginator = Paginator(user_projects, count)
        project_page_number = request.GET.get('page')
        project_page_obj = project_paginator.get_page(project_page_number)

        context = {
            "user":request.user,
            "projectForm": ProjectForm(),
            "apiSettingsForm": ApiSettingsForm(request=request),
            "projects": project_page_obj,
            'total_projects': total_projects,
            'approved_projects': approved_projects,
            'pending_projects': pending_projects,
        }
        return render(request, template, context)
    elif user.user_type == "manager":
        User = get_user_model()
        
        users = User.objects.filter(user_type__in=['partner', 'advertiser']
        )
        count = 10
        users_paginator = Paginator(users, 4)
        users_page_number = request.GET.get('page')
        users_page_obj = users_paginator.get_page(users_page_number)

        new_users = User.objects.filter(
            date_joined__gte=timezone.now() - timedelta(days=1)
        ).count()


        pending_projects = Project.objects.filter(status='На модерации').order_by('-created_at')
        pending_platforms = Platform.objects.filter(status='На модерации').order_by('-created_at')
        pending_list = list(pending_projects) + list(pending_platforms)
        pending_paginator = Paginator(pending_list, count)
        pending_page_number = request.GET.get('page')
        pending_page_obj = pending_paginator.get_page(pending_page_number)

        context = {
            "user":request.user,
            "users":users_page_obj,
            "pending_items": pending_page_obj,
            "pending_items_len": len(pending_list),
            "new_users_count":new_users
        }
        return render(request, template,context)
    


