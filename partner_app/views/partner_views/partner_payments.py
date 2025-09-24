from django.conf import settings
from django.shortcuts import render,redirect
from django.db.models import Sum

from partner_app.models import PartnerTransaction,PartnerActivity
from partner_app.utils import _paginate

def partner_payments(request):  
    """подключенные проекты партнёра"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')    
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    notifications_count = PartnerActivity.objects.filter(partner=request.user.partner_profile,is_read=False).count()
    
    total_proccessing_payments = PartnerTransaction.objects.filter(
        status=PartnerTransaction.STATUS_CHOICES.PENDING
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    total_paid = PartnerTransaction.objects.filter(
        status=PartnerTransaction.STATUS_CHOICES.COMPLETED
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    transactions = PartnerTransaction.objects.filter(partner=request.user).order_by('-date')
    transactions_page = _paginate(request,transactions,5,'transactions_page')
    context = {
        "notifications_count":notifications_count,
        
        "total_proccessing_payments":total_proccessing_payments,
        "total_paid":total_paid,
        
        "transactions_page": transactions_page,
        
        "is_payout_available": request.user.partner_profile.balance > float(settings.PARTNER_PAYOUT_SETTINGS["min_amount"]),
        "min_payout": settings.PARTNER_PAYOUT_SETTINGS["min_amount"],
        "fee_percent": settings.PARTNER_PAYOUT_SETTINGS["fee_percent"],
    }
    
    return render(request, 'partner_app/dashboard/partner/payments/payments.html',context=context)