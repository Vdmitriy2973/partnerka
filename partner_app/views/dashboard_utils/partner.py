from datetime import date
from dateutil.relativedelta import relativedelta
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render
from django.db.models import Count, F, FloatField, ExpressionWrapper, Sum,Value
from django.db.models.functions import Coalesce

from partner_app.models import Platform, Project, PartnerLink, PartnerActivity
from partner_app.forms import PlatformForm
from .common import _apply_search, _paginate

def handle_partner_dashboard(request):
    """Обработчик личного кабинета партнера"""
    
    # Платформы
    platforms = Platform.objects.filter(
            partner=request.user).annotate(
        conversions_total=Coalesce(Sum('conversions__amount'), Value(Decimal(0.0))),
        conversion_count=Coalesce(Count('conversions'),Value(0))
    ).order_by('-created_at')
    
    # Партнёрские ссылки 
    partner_links = PartnerLink.objects.filter(partner=request.user).annotate(
        conversions_total=Coalesce(Sum('conversions__amount'), Value(Decimal(0.0)))
    ).order_by('-created_at')
    
    last_activity = PartnerActivity.objects.filter(partner=request.user.partner_profile).order_by('-created_at')[:5]
    
    # Получаем параметры поиска
    platforms_search_q = request.GET.get('platforms_search', '').strip()
    projects_search_q = request.GET.get('offers_search', '').strip()
    connection_search_q = request.GET.get('connections_search', '').strip()
        
    # Применение поиска
    available_projects = _get_available_projects(request)        
    connected_projects = _get_connected_projects(request)
    
    if platforms_search_q:
        platforms = _apply_search(platforms, platforms_search_q, ['name'])
    if projects_search_q:
        available_projects = _apply_search(available_projects, projects_search_q, ['name'])
    if connection_search_q:
        connected_projects = _apply_search(connected_projects, connection_search_q, ['name'])
        
    # Получаем агрегированные данные
    total_platforms = platforms.count()
    approved_platforms_count = platforms.filter(status='Подтверждено').count()
    pending_platforms = platforms.filter(status='На модерации').count()
    rejected_platforms = platforms.filter(status='Отклонено').count()
    total_projects = available_projects.count()
    
    approved_platforms = platforms.filter(status='Подтверждено')
    
    total_connected_projects = connected_projects.count()
    active_connected_projects = connected_projects.filter(
        partner_memberships__status="Активен"
    ).count()
    suspended_connected_projects = connected_projects.filter(
        partner_memberships__status="Приостановлен"
    ).count()
    
    active_links = PartnerLink.objects.filter(
        partner=request.user,
        is_active=True
    ).count()
    
    best_link = PartnerLink.objects.annotate(
        clicks_count=Count('clicks'),
        conversions_count=Count('conversions'),
            score=ExpressionWrapper(
                F('conversions_count') * 0.5 + F('clicks_count') * 0.3,
                output_field=FloatField()
            )
        ).filter(
            is_active=True
    ).order_by('-score').first()
    
    clicks_count = request.user.clicks.count()
    if not best_link:
        best_link = "Отсутствует"
    if clicks_count == 0:
        conversion = 0
    else:
        conversion =  f"{(request.user.conversions.count() / request.user.clicks.count()) * 100:.2f}"
    
    # Пагинация
    platform_page = _paginate(request, platforms, 5, 'platforms_page')
    available_projects_page = _paginate(request, available_projects, 6, 'projects_page')
    connected_projects_page = _paginate(request, connected_projects, 6, 'connected_projects_page')

    context = {
        
            "user": request.user,  
            "int_balance":int(request.user.partner_profile.balance),
            'platformForm': PlatformForm(),
            'platforms': platform_page,
            'total_platforms': total_platforms,
            'approved_platforms': approved_platforms,
            'approved_platforms_count': approved_platforms_count,
            'pending_platforms_count': pending_platforms,
            "rejected_platforms_count":rejected_platforms,
            
            "offers_search_query": projects_search_q,
            "connection_search_query": connection_search_q,
            "platforms_search_query": platforms_search_q,
            
            'projects': available_projects_page,
            'total_projects': total_projects,
            "connected_projects": connected_projects_page,
            "active_connected_projects": active_connected_projects,
            "suspended_connected_projects":suspended_connected_projects,
            "total_connected_projects": total_connected_projects,
            
            "partner_links":partner_links,
            
            "clicks_count":clicks_count,
            "conversion":conversion,
            "active_links":active_links,
            "best_link":best_link,
            
            "last_activity":last_activity,
            
            "min_payout": settings.PARTNER_PAYOUT_SETTINGS["min_amount"],
            "fee_percent": settings.PARTNER_PAYOUT_SETTINGS["fee_percent"],
            "payout_info":get_next_payout_date(),
            'is_payout_today': date.today().day in [1,15],
            "days_until_payment":get_days_until_payout(),
    }
    return render(request, 'partner_app/dashboard/partner.html', context)

def _get_available_projects(request):
    """Получение доступных проектов с оптимизацией"""
    return Project.objects.filter(
        status=Project.StatusType.APPROVED,
        is_active=True
    ).exclude(
        partners=request.user 
    ).select_related(
        'advertiser' 
    ).order_by('-created_at')
    
def _get_connected_projects(request):
    """Получение подключенных проектов"""
    return Project.objects.prefetch_related('params', 'partner_memberships','project_links',"conversions").filter(
        partner_memberships__partner=request.user
    ).annotate(
        conversions_total=Coalesce(Sum('conversions__amount'), Value(Decimal(0.0)))
    ).order_by('-partner_memberships__joined_at').distinct()
    
def get_next_payout_date():
    today = date.today()
    
    if today.day > 15:
        # Если сегодня после 15 числа - следующая выплата 1 числа следующего месяца
        next_payout = date(today.year, today.month, 1) + relativedelta(months=1)
    elif today.day > 1:
        # Если сегодня между 1 и 15 - следующая выплата 15 текущего месяца
        next_payout = date(today.year, today.month, 15)
    else:
        # Если сегодня 1 число - выплата сегодня
        next_payout = today
    
    return next_payout

def get_days_until_payout():
    today = date.today()
    if today.day > 15:
        # Если сегодня после 15 числа - следующая выплата 1 числа следующего месяца
        day = today.day - 1
    elif today.day > 1:
        # Если сегодня между 1 и 15 - следующая выплата 15 текущего месяца
        day = 15 - today.day
    elif today.day == 1 or today.day == 15:
        day = today
    
    return day