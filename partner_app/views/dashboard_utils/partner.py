from django.shortcuts import render
from django.db.models import Count, Case, When, IntegerField

from traceback import format_exc

from partner_app.models import Platform, Project
from partner_app.forms import PlatformForm
from .common import _apply_search, _paginate

def handle_partner_dashboard(request):
    """Обработчик личного кабинета партнера"""
    # Основные QuerySets с оптимизацией
    platforms = Platform.objects.filter(
            partner=request.user
        ).select_related('partner').annotate(
            total=Count('id'),
            approved=Count(Case(When(status='Подтверждено', then=1), output_field=IntegerField())),
            pending=Count(Case(When(status='На модерации', then=1), output_field=IntegerField()))
        ).order_by('-created_at')
        
        # Получаем параметры поиска
    platforms_search_q = request.GET.get('platforms_search', '').strip()
    projects_search_q = request.GET.get('offers_search', '').strip()
    connection_search_q = request.GET.get('connections_search', '').strip()
        
        # Применение поиска
    if platforms_search_q:
        platforms = _apply_search(platforms, platforms_search_q, ['name'])
        
    projects = _get_available_projects(request)
    if projects_search_q:
        projects = _apply_search(projects, projects_search_q, ['name'])
        
    connected_projects = _get_connected_projects(request)
    if connection_search_q:
        connected_projects = _apply_search(connected_projects, connection_search_q, ['name'])
        
        # Получаем агрегированные данные
    total_platforms = platforms.count()
    approved_platforms = platforms.filter(status='Подтверждено').count()
    pending_platforms = platforms.filter(status='На модерации').count()
    rejected_platforms = platforms.filter(status='Отклонено').count()
    total_projects = projects.count()
    total_connected_projects = connected_projects.count()
    active_connected_projects = connected_projects.filter(
        partner_memberships__status="Активен"
    ).count()
    suspended_connected_projects = connected_projects.filter(
        partner_memberships__status="Приостановлен"
    ).count()
        
        # Пагинация
    platform_page = _paginate(request, platforms, 5, 'platforms_page')
    projects_page = _paginate(request, projects, 6, 'projects_page')
    connected_projects_page = _paginate(request, connected_projects, 6, 'connected_projects_page')

    context = {
            "user": request.user,  
            'platformForm': PlatformForm(),
            'platforms': platform_page,
            'approved_platforms': approved_platforms,
            'pending_platforms': pending_platforms,
            "offers_search_query": projects_search_q,
            "connection_search_query": connection_search_q,
            "platforms_search_query": platforms_search_q,
            'total_platforms': total_platforms,
            "rejected_platforms":rejected_platforms,
            'projects': projects_page,
            'total_projects': total_projects,
            "connected_projects": connected_projects_page,
            "active_connected_projects": active_connected_projects,
            "suspended_connected_projects":suspended_connected_projects,
            "total_connected_projects": total_connected_projects,
    }
        
    return render(request, 'partner_app/dashboard/partner.html', context)

def _get_available_projects(request):
    """Получение доступных проектов с оптимизацией"""
    return Project.objects.filter(
        status='Подтверждено',
        is_active=True
    ).exclude(
        partner_memberships__partner=request.user
    ).select_related('advertiser')

def _get_connected_projects(request):
    """Получение подключенных проектов"""
    return Project.objects.filter(
        partner_memberships__partner=request.user
    ).prefetch_related(
        'partner_memberships'
    ).distinct().order_by('-partner_memberships__joined_at')