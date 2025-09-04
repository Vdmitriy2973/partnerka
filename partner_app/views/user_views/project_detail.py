from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Value, Q,Count,OuterRef,Subquery
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from partner_app.models import ProjectPartner,Project, Conversion

@login_required
def project_detail(request, project_id):
    """Информация о проекте"""
    
    try:
        # Проект
        project = get_object_or_404(Project,id=project_id)

        # Получаем статистику по партнёрам проекта
        partnership_stats = (
            ProjectPartner.objects
            .filter(project=project)
            .select_related('partner')
            .annotate(
                conversions_total=Coalesce(
                    Sum(
                        'conversions__amount',
                        filter=Q(conversions__project_id=project.id)
                    ),
                    Value(Decimal('0.00'))
                ),
                conversions_count=Coalesce(
                    Count(
                        'conversions',
                        filter=Q(conversions__project_id=project.id)
                    ),
                    Value(0)
                )
            )
            .order_by('-joined_at')
        )

        partners_search_q = request.GET.get('partners_search','').strip()
        if partners_search_q:
            partnership_stats = partnership_stats.filter(
            Q(partner__username__icontains=partners_search_q)
        )
        # Пагинация
        paginator = Paginator(partnership_stats, 5)
        page_number = request.GET.get('partners_page')
        partnerships = paginator.get_page(page_number)
        
        # Общая статистика по проекту
        total_partners = partnership_stats.count()
        active_partners = partnership_stats.filter(status=ProjectPartner.StatusType.ACTIVE).count()
        
        return render(request, 'partner_app/projects/project_details.html', {
            'partners_search_q':partners_search_q,
            'project': project,
            'partnerships': partnerships,
            'total_partners': total_partners,
            'active_partners': active_partners
        })

    except Exception as e:
        messages.error(request, message="Произошла ошибка при загрузке страницы проекта")
        if hasattr(request.user, 'advertiserprofile'): 
            return redirect('advertiser_dashboard')
        return redirect('dashboard')