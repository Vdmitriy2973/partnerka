from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.shortcuts import render

from partner_app.models import Project
from partner_app.forms import ProjectForm, ApiSettingsForm
from .common import _paginate, _apply_search

def handle_advertiser_dashboard(request):
    """Оптимизированный обработчик личного кабинета рекламодателя"""
    User = get_user_model()
    
    
    # Получаем параметры запроса
    projects_search_q = request.GET.get('projects_search', '').strip()
    partners_search_q = request.GET.get('partners_search', '').strip()
    
    # Партнеры с аннотациями и оптимизацией
    partners = User.objects.filter(
        project_memberships__project__advertiser=request.user
    ).distinct()
    
    projects = Project.objects.filter(
        advertiser=request.user
    ).select_related('advertiser').order_by('-created_at')

    if partners_search_q:
        partners = _apply_search(partners,partners_search_q,["email"])

    if projects_search_q:
        projects = _apply_search(projects, projects_search_q,['name'])

    # Получаем все счетчики статусов проектов
    status_counts = {
        'total': projects.count(),
        'approved': projects.filter(status='Подтверждено').count(),
        'pending': projects.filter(status='pending').count(),
        'active_approved': projects.filter(status='Подтверждено', is_active=True).count()
    }

    # Применяем универсальную пагинацию
    projects_page = _paginate(request, projects, 6, 'projects_page')
    partners_page = _paginate(request, partners, 6, 'partners_page')
    
    context = {
        "user": request.user,
        "projectForm": ProjectForm(),
        "apiSettingsForm": ApiSettingsForm(request=request),
        "projects": projects_page,
        "user_projects_count": status_counts.get('active_approved', 0),
        'total_projects': status_counts.get('total', 0),
        'approved_projects': status_counts.get('approved', 0),
        'pending_projects': status_counts.get('pending', 0),
        'partners_search_query':partners_search_q,
        "partners": partners_page,
        "partners_count": partners.count()
    }
    
    return render(request, "partner_app/dashboard/advertiser.html", context)