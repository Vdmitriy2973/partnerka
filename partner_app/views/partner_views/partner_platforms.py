from decimal import Decimal

from django.shortcuts import render,redirect
from django.db.models import Count, Sum,Value
from django.db.models.functions import Coalesce

from partner_app.forms import PlatformForm
from partner_app.models import Platform,PartnerActivity
from partner_app.utils import _paginate, _apply_search

def partner_platforms(request):  
    """Площадки партнёра"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    notifications_count = PartnerActivity.objects.filter(partner=request.user.partner_profile,is_read=False).count()
    
    platforms_search_q = request.GET.get('platforms_search', '').strip()
    
    platforms = Platform.objects.filter(
            partner=request.user).annotate(
        conversions_total=Coalesce(Sum('conversions__amount'), Value(Decimal(0.0))),
        conversion_count=Coalesce(Count('conversions'),Value(0))
    ).order_by('-created_at')
    
    total_platforms = platforms.count()
    approved_platforms = platforms.filter(status='Подтверждено').count()
    pending_platforms = platforms.filter(status='На модерации').count()
    rejected_platforms = platforms.filter(status='Отклонено').count()
    
    if platforms_search_q:
        platforms = _apply_search(platforms, platforms_search_q, ['name'])
        
    platform_page = _paginate(request, platforms, 5, 'platforms_page')
    
    context = {
        'notifications_count':notifications_count,
        
        'platformForm': PlatformForm(),
        
        "platforms":platform_page,
        
        "total_platforms": total_platforms,
        "approved_platforms_count": approved_platforms,
        "pending_platforms_count":pending_platforms,
        "rejected_platforms_count":rejected_platforms,
        
        "platforms_search_query": platforms_search_q,
    }
    
    return render(request, 'partner_app/dashboard/partner/platforms/platforms.html',context=context)