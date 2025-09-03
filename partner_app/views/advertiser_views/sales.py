import json 

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg

from partner_app.utils import _paginate
from partner_app.models import Conversion

@login_required
def advertiser_sales(request):
    
    conversions = Conversion.objects.filter(advertiser=request.user.advertiserprofile).select_related("project","partner").order_by("-created_at")
    conversions_count = conversions.count()
    
    if conversions:
        chart_data = [
        {
            "id": conv.id,
            "project": conv.project.name if conv.project else None, 
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
    
    conversions_page = _paginate(request,conversions,6,'conversions_page')
    
    context = {
        "conversions":conversions_page,
        "conversions_count":conversions_count,
        "conversions_average":conversions_average,
        "conversions_total":conversions_total,
        "conversions_json": json.dumps(chart_data),
        
    }
    return render(request, 'partner_app/dashboard/new_advertiser/sales/sales.html',context=context)