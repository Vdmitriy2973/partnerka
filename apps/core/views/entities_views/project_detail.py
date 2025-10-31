from decimal import Decimal

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Value, Q,Count,OuterRef,DecimalField,IntegerField,Subquery
from django.db.models.functions import Coalesce
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from apps.partnerships.models import ProjectPartner
from apps.advertisers.models import Project
from apps.tracking.models import Conversion

@login_required
def project_detail(request, project_id):
    """Информация о проекте"""
    
    try:
        
        project = get_object_or_404(Project,id=project_id)
        
        conversion_amount_subquery = Conversion.objects.filter(
            partnership=OuterRef('pk')
        ).values('partnership').annotate(
            total=Sum('amount')
        ).values('total')[:1]


        conversion_count_subquery = Conversion.objects.filter(
            partnership=OuterRef('pk')
        ).values('partnership').annotate(
            count=Count('id')
        ).values('count')[:1]

        partnership_stats = (
            ProjectPartner.objects
            .filter(project=project)
            .select_related('partner')
            .annotate(
                conversions_total=Coalesce(
                    Subquery(conversion_amount_subquery),
                    Value(Decimal('0.00')),
                    output_field=DecimalField(max_digits=10, decimal_places=2)
                ),
                conversions_count=Coalesce(
                    Subquery(conversion_count_subquery),
                    Value(0),
                    output_field=IntegerField()
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
        
        return render(request, 'core/entities/project/project_details.html', {
            'partners_search_q':partners_search_q,
            'project': project,
            'partnerships': partnerships,
            'total_partners': total_partners,
            'active_partners': active_partners
        })

    except Exception as e:
        print(e)
        messages.error(request, message="Произошла ошибка при загрузке страницы проекта")
        if hasattr(request.user, 'advertiserprofile'): 
            return redirect('advertiser_dashboard')
        return redirect('dashboard')