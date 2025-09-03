from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Value, Q,Count
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from partner_app.models import ProjectPartner,Project
from partner_app.views.dashboard_utils.common import _paginate

@login_required
def project_detail(request, project_id):
    # Основная информация о проекте
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
            Q(partner__username__icontains=partners_search_q) |
            Q(partner__first_name__icontains=partners_search_q) |
            Q(partner__last_name__icontains=partners_search_q) |
            Q(partner__email__icontains=partners_search_q) | 
            Q(partner__phone__icontains=partners_search_q) 
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
        # Логирование ошибки (можно настроить логирование)
        print(f"Error in project_detail: {e}")
        messages.error(request, message="Произошла ошибка при загрузке страницы проекта")
        return redirect('dashboard')  # Перенаправление на главную