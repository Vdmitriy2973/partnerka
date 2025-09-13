from decimal import Decimal

from django.shortcuts import render,redirect
from django.db.models import Count, F, FloatField, ExpressionWrapper, Sum,Value, Prefetch, DecimalField,Q
from django.db.models.functions import Coalesce


from partner_app.models import PartnerLink
from partner_app.utils import _paginate

def partner_links(request):  
    """подключенные проекты партнёра"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    
    active_links = PartnerLink.objects.filter(
        partner=request.user,
        is_active=True
    ).count()
    
    clicks_count = request.user.partner_profile.clicks.count()
    
    if clicks_count == 0:
        conversion = 0
    else:
        conversion =  f"{(request.user.partner_profile.conversions.count() / request.user.partner_profile.clicks.count()) * 100:.2f}"
    
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
    
    partner_links = PartnerLink.objects.filter(partner=request.user).annotate(
        conversions_total=Coalesce(Sum('conversions__amount'), Value(Decimal(0.0)))
    ).order_by('-created_at')
    
    partner_links_page = _paginate(request, partner_links, 6, 'partner_links_page')
    
    context = {
        "clicks_count": clicks_count,
        "active_links":active_links,
        "conversion":conversion,
        "best_link":best_link,
        "partner_links":partner_links_page
    }
    
    return render(request, 'partner_app/dashboard/partner/links/links.html',context=context)