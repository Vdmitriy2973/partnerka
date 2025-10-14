from datetime import timedelta

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg,Sum
from django.db.models.functions import Round
from django.utils import timezone

from apps.partners.models import Platform
from apps.tracking.models import Conversion

@login_required
def platform_detail(request, platform_id):
    try:
        platform = get_object_or_404(Platform, id=platform_id)

        revenue_info = Conversion.objects.filter(platform=platform).aggregate(avg_revenue=Round(Avg('amount'),2),total_revenue=Round(Sum('amount'),2))

        today = timezone.now().date()
        first_day_of_current_month = today.replace(day=1)
        last_day_of_last_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_last_month = last_day_of_last_month.replace(day=1)

        total_revenue_last_month = Conversion.objects.filter(
            created_at__date__gte=first_day_of_last_month,
            created_at__date__lte=last_day_of_last_month
        ).aggregate(total_revenue=Sum('amount'))['total_revenue'] or 0


        context = {
            "platform":platform,
            "revenue_info":revenue_info,
            "total_revenue_last_month":total_revenue_last_month
        }
        
        return render(request, 'core/entities/platform/platform_details.html', context)
    
    except Exception as e:
        # Логирование ошибки (можно настроить логирование)
        print(f"Error in partner_detail: {e}")
        messages.error(request, message="Произошла ошибка при загрузке профиля партнера")
        if hasattr(request.user, 'advertiserprofile'): 
            return redirect('advertiser_dashboard')
        return redirect('dashboard')    