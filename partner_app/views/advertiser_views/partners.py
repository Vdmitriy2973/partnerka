from decimal import Decimal

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Coalesce
from django.db.models import Sum, Count, OuterRef, Subquery,Value

from partner_app.models import User,Conversion
from partner_app.views.utils import _paginate,_apply_search

@login_required
def advertiser_partners(request):
    
    conversions_total_subquery = Subquery(
        Conversion.objects.filter(partner=OuterRef('id'))
        .values('partner')
        .annotate(total=Sum('amount'))
        .values('total')[:1]
    )

    conversions_count_subquery = Subquery(
        Conversion.objects.filter(partner=OuterRef('id'))
        .values('partner')
        .annotate(count=Count('id'))
        .values('count')[:1]
    )
    
    partners = User.objects.filter(
        project_memberships__project__advertiser=request.user
    ).annotate(
        conversions_total=Coalesce(conversions_total_subquery,Value(Decimal(0))),
        conversions_count=Coalesce(conversions_count_subquery,Value(0))
    ).distinct().order_by("-date_joined")
    
    partners_search_q = request.GET.get('partners_search', '').strip()
    
    if partners_search_q:
        partners = _apply_search(partners,partners_search_q,["username"])
    
    partners_page = _paginate(request, partners, 6, 'partners_page')
    
    context = {
        "partners":partners_page,
        'partners_search_query':partners_search_q,
    }
    return render(request, 'partner_app/dashboard/new_advertiser/partners/partners.html',context=context)