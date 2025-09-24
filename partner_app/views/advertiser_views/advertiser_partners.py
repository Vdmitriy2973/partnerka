from decimal import Decimal

from django.shortcuts import render, redirect
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count, Value,DecimalField, Q

from partner_app.models import User, AdvertiserActivity
from partner_app.views.utils import _paginate,_apply_search

def advertiser_partners(request):
    """Страница с подключенными партнёрами рекламодателя"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    notifications_count = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile,is_read=False).count()
    
    partners = User.objects.filter(
        project_memberships__project__advertiser=request.user
    ).annotate(
        conversions_total=Coalesce(
            Sum('partner_profile__conversions__amount', 
                filter=Q(partner_profile__conversions__project__advertiser=request.user)),
            Value(Decimal(0)),
            output_field=DecimalField(max_digits=10, decimal_places=2)
        ),
        conversions_count=Coalesce(
            Count('partner_profile__conversions',
                filter=Q(partner_profile__conversions__project__advertiser=request.user)),
            Value(0)
        )
    ).distinct().order_by("-date_joined")
    partners_search_q = request.GET.get('partners_search', '').strip()
    
    if partners_search_q:
        partners = _apply_search(partners,partners_search_q,["username"])
    
    partners_page = _paginate(request, partners, 6, 'partners_page')
    
    context = {
        "notifications_count":notifications_count,
        
        "partners":partners_page,
        'partners_search_query':partners_search_q,
    }
    return render(request, 'partner_app/dashboard/advertiser/partners/partners.html',context=context)