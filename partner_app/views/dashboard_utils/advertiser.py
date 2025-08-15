from decimal import Decimal
import json 

from django.db.models import Sum, Count, Avg, OuterRef, Subquery,Value
from django.shortcuts import render
from django.db.models.functions import Coalesce

from partner_app.models import Project, Conversion,User, AdvertiserActivity, ClickEvent
from partner_app.forms import ProjectForm, ApiSettingsForm, ProjectParamForm
from .common import _paginate, _apply_search

def handle_advertiser_dashboard(request):
    """Оптимизированный обработчик личного кабинета рекламодателя"""    
    # Получаем параметры запроса
    projects_search_q = request.GET.get('projects_search', '').strip()
    partners_search_q = request.GET.get('partners_search', '').strip()
    
    # Партнеры с аннотациями и оптимизацией
    conversions_total_subquery = Subquery(
        Conversion.objects.filter(partner=OuterRef('id'))
        .values('partner')
        .annotate(total=Sum('amount'))
        .values('total')[:1]
    )

    conversions_count_subquery = Subquery(
        Conversion.objects.filter(partner=OuterRef('id'))
        .values('partner_id')
        .annotate(count=Count('id'))
        .values('count')[:1]
    )

    partners = User.objects.filter(
        project_memberships__project__advertiser=request.user
    ).annotate(
        conversions_total=Coalesce(conversions_total_subquery,Value(Decimal(0))),
        conversions_count=Coalesce(conversions_count_subquery,Value(0))
    ).distinct().order_by("-date_joined")
    
    projects = Project.objects.filter(
        advertiser=request.user
    ).select_related('advertiser').order_by('-created_at')

    last_activity = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile).order_by('-created_at')[:5]
    conversions = Conversion.objects.filter(project__advertiser=request.user).select_related("project").order_by("-created_at")
    conversions_count = conversions.count()
    clicks_count = ClickEvent.objects.filter(project__advertiser=request.user).count()
    conversion_percent = 0
    if clicks_count > 0:
        conversion_percent =  f"{(conversions_count / clicks_count) * 100:.2f}"
    
    chart_data = None
    if conversions:
        chart_data = [
        {
            "id": conv.id,
            "project": conv.project.name, 
            "date": conv.created_at.strftime("%d-%m-%y"),  
            "amount": float(conv.amount) 
        }
        for conv in conversions
    ]
        conversions_average = f"{conversions.aggregate(avg_price=Avg('amount'))["avg_price"]:.2f}"
        conversions_total = f"{conversions.aggregate(total_price=Sum('amount'))["total_price"]:.2f}"
    else:
        conversions_total = 0
        conversions_average = 0
    
    
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
    conversions_page = _paginate(request,conversions,6,'conversions_page')
    
    context = {
        "user": request.user,
        "projectForm": ProjectForm(),
        'projectParamForm':ProjectParamForm(),
        "apiSettingsForm": ApiSettingsForm(request=request),
        "projects": projects_page,
        "user_projects_count": status_counts.get('active_approved', 0),
        'total_projects': status_counts.get('total', 0),
        'approved_projects': status_counts.get('approved', 0),
        'pending_projects': status_counts.get('pending', 0),
        'partners_search_query':partners_search_q,
        "partners": partners_page,
        "partners_count": partners.count(),
        
        "conversions":conversions_page,
        "conversions_count":conversions_count,
        "conversion_percent":conversion_percent,
        "conversions_average":conversions_average,
        "conversions_total":conversions_total,
        "conversions_json": json.dumps(chart_data),
        
        "last_activity":last_activity,
        "clicks_count":clicks_count,
    }
    
    return render(request, "partner_app/dashboard/advertiser.html", context)