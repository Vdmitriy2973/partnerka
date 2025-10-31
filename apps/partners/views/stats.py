from datetime import timedelta
import json 

from django.shortcuts import render,redirect
from django.db.models import Count, F, FloatField, ExpressionWrapper, Sum,Avg
from django.db.models.functions import TruncDate
from django.utils import timezone

from apps.partners.models import PartnerActivity,Platform
from apps.partnerships.models import ProjectPartner
from apps.tracking.models import Conversion,ClickEvent
from utils import _paginate

def stats(request):
    """Статистика партнёра"""

    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(user,"partner_profile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    conversions = Conversion.objects.filter(
        partner=user.partner_profile
        ).select_related(
            "project","platform"
            ).only(
                'id',
                'project',
                'platform',
                'created_at',
                'amount'
            ).order_by(
                "-created_at")
    conversions_count = conversions.count()
    conversions_page = _paginate(request,conversions,6,'conversions_page')

    clicks = ClickEvent.objects.filter(partner=user.partner_profile).order_by('-created_at') 
    clicks_count = clicks.count()

    last_30_days = timezone.now() - timedelta(days=30)
    # Агрегируем конверсии по дням
    conversions_by_day = Conversion.objects.filter(
        partner=user.partner_profile,
        created_at__gte=last_30_days
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Агрегируем клики по дням
    clicks_by_day = ClickEvent.objects.filter(
        partner=user.partner_profile,
        created_at__gte=last_30_days
    ).annotate(
        date=TruncDate('created_at')
    ).values('date').annotate(
        count=Count('id')
    ).order_by('date')

    # Создаем словари для быстрого доступа
    conversions_dict = {item['date']: item['count'] for item in conversions_by_day}
    clicks_dict = {item['date']: item['count'] for item in clicks_by_day}

    # Генерируем все даты за период
    all_dates = []
    current_date = last_30_days.date()
    while current_date <= timezone.now().date():
        all_dates.append(current_date)
        current_date += timedelta(days=1)

    # Формируем данные для Chart.js
    chart_data = {
        'labels': [date.strftime("%d-%m-%y") for date in all_dates],
        'datasets': [
            {
                'label': 'Конверсии',
                'data': [conversions_dict.get(date, 0) for date in all_dates],
                'borderColor': 'rgb(75, 192, 192)',
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'tension': 0.1
            },
            {
                'label': 'Клики', 
                'data': [clicks_dict.get(date, 0) for date in all_dates],
                'borderColor': 'rgb(255, 99, 132)',
                'backgroundColor': 'rgba(255, 99, 132, 0.2)',
                'tension': 0.1
            }
        ]
    }

    
    last_month = timezone.now() - timedelta(days=30)

    total_revenue = Conversion.objects.filter(partner=user.partner_profile).aggregate(total=Sum('amount'))['total'] or 0
    total_revenue_last_month = Conversion.objects.filter(partner=user.partner_profile,created_at__gte=last_month).aggregate(total=Sum('amount'))['total'] or 0
    average_revenue = f"{Conversion.objects.filter(partner=user.partner_profile).aggregate(total=Avg('amount'))['total']:.2f}" or 0

    top_partnerships = ProjectPartner.objects.filter(
        partner=user
    ).select_related(
        'project', 'partner'
    ).prefetch_related(
        'conversions'
    ).annotate(
        total_amount=Sum('conversions__amount'),
        conversion_count=Count('conversions__amount'),
        score=ExpressionWrapper(
                F('conversion_count') * 0.5 + F('total_amount') * 0.3,
                output_field=FloatField()
            )
        ).order_by('score')[:4]
    
    for partnership in top_partnerships:
        clicks = partnership.clicks.count()
        if clicks == 0:
            partnership.cr = 0
        else:
            partnership.cr = f"{(partnership.conversions.count() / clicks) * 100:.2f}"

    top_platforms = Platform.objects.filter(
        conversions__partner=user.partner_profile,
        ).annotate(
            total_revenue = Sum('conversions__amount',distinct=True),
            click_count=Count('clicks', distinct=True),
            conversion_count=Count('conversions', distinct=True),
            score=ExpressionWrapper(
                F('conversion_count') * 0.5 + F('click_count') * 0.3,
                output_field=FloatField()
            )
        ).filter(
            is_active=True
    ).order_by('-score')[:4]

    notifications_count = PartnerActivity.objects.filter(partner=user.partner_profile,is_read=False).count()
    
    context = {
        'notifications_count':notifications_count,

        "conversions":conversions_page,
        "conversions_count":conversions_count,

        "clicks":clicks,
        "clicks_count":clicks_count,

        "total_revenue":total_revenue,
        "total_revenue_last_month":total_revenue_last_month,
        "average_revenue": average_revenue,

        "top_partnerships": top_partnerships,
        "top_platforms": top_platforms,

        "conversions_json": json.dumps(chart_data) if chart_data else None,
    }
    
    return render(request, 'partners/stats/stats.html',context=context)