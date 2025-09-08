from decimal import Decimal
import json

from django.conf import settings
from django.shortcuts import render
from django.db.models import Count, F, FloatField, ExpressionWrapper, Sum,Value, Prefetch, DecimalField,Q
from django.db.models.functions import Coalesce

from partner_app.models import Platform, Project, PartnerLink, PartnerActivity, PartnerTransaction,ProjectPartner
from partner_app.forms import PlatformForm
from .common import _apply_search, _paginate

def handle_partner_dashboard(request):
    """Обработчик личного кабинета партнера"""
    
    user = request.user
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
    for project in connected_projects:
        project.has_link = project.has_partner_link(user)
        project.params_json = json.dumps(list(
            project.params.all().values('name', 'description', 'param_type', 'example_value')
        ))
    
        
    # Получаем агрегированные данные
    total_platforms = platforms.count()
    approved_platforms_count = platforms.filter(status='Подтверждено').count()
    pending_platforms = platforms.filter(status='На модерации').count()
    rejected_platforms = platforms.filter(status='Отклонено').count()
    total_projects = available_projects.count()
    
    if platforms_search_q:
        platforms = _apply_search(platforms, platforms_search_q, ['name'])
    if projects_search_q:
        available_projects = _apply_search(available_projects, projects_search_q, ['name'])
    if connection_search_q:
        connected_projects = _apply_search(connected_projects, connection_search_q, ['name'])
    
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
    
    best_link = PartnerLink.objects.filter(partner=request.user).annotate(
        clicks_count=Count('clicks'),
        conversions_count=Count('conversions'),
            score=ExpressionWrapper(
                F('conversions_count') * 0.5 + F('clicks_count') * 0.3,
                output_field=FloatField()
            )
        ).filter(
            is_active=True
    ).order_by('-score').first()
    
    transactions = PartnerTransaction.objects.filter(partner=request.user).order_by('-date')
    total_paid = PartnerTransaction.objects.filter(
        status=PartnerTransaction.STATUS_CHOICES.COMPLETED
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    total_proccessing_payments = PartnerTransaction.objects.filter(
        status=PartnerTransaction.STATUS_CHOICES.PENDING
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    clicks_count = request.user.partner_profile.clicks.count()
    if not best_link:
        best_link = "Отсутствует"
    if clicks_count == 0:
        conversion = 0
    else:
        conversion =  f"{(request.user.partner_profile.conversions.count() / request.user.partner_profile.clicks.count()) * 100:.2f}"
    
    # Пагинация
    platform_page = _paginate(request, platforms, 5, 'platforms_page')
    available_projects_page = _paginate(request, available_projects, 6, 'projects_page')
    connected_projects_page = _paginate(request, connected_projects, 5, 'connected_projects_page')
    transactions_page = _paginate(request,transactions,5,'transactions_page')
    
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
            
            "is_payout_available": request.user.partner_profile.balance > float(settings.PARTNER_PAYOUT_SETTINGS["min_amount"]),
            "min_payout": settings.PARTNER_PAYOUT_SETTINGS["min_amount"],
            "fee_percent": settings.PARTNER_PAYOUT_SETTINGS["fee_percent"],
            
            'transactions_page':transactions_page,
            'total_paid':total_paid,
            'total_proccessing_payments':total_proccessing_payments
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
    """Получение подключенных проектов у партнёра"""
    user_memberships_prefetch = Prefetch(
        'partner_memberships',
        queryset=ProjectPartner.objects.filter(partner=request.user),
        to_attr='user_memberships'
    )
    
    return Project.objects.filter(
        partner_memberships__partner=request.user
    ).prefetch_related(
        'params',
        user_memberships_prefetch,
        'project_links',
        'conversions'
    ).annotate(
        conversions_total=Coalesce(
            Sum('conversions__amount',filter=Q(conversions__partner=request.user.partner_profile), output_field=DecimalField(max_digits=10, decimal_places=2)),
            Value(Decimal('0.00'))
        )
    ).order_by('-partner_memberships__joined_at')