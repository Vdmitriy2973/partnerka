from django.shortcuts import render,redirect

from .common import _get_available_projects
from utils import _paginate
from partner_app.models import PartnerActivity

def partner_offers(request):  
    """Доступные предложения"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    projects_search_q = request.GET.get('offers_search', '').strip()
    
    notifications_count = PartnerActivity.objects.filter(partner=request.user.partner_profile,is_read=False).count()
    available_projects = _get_available_projects(request)     
    total_projects = available_projects.count()
    
    available_projects_page = _paginate(request, available_projects, 6, 'projects_page')
    context = {
        "notifications_count":notifications_count,
        
        "offers_search_query": projects_search_q,
        "total_projects":total_projects,
        'projects': available_projects_page,
    }
    
    return render(request, 'partner_app/dashboard/partner/offers/offers.html',context=context)