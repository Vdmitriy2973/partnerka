from django.shortcuts import render,redirect

from .common import _get_available_projects
from partner_app.utils import _paginate

def partner_offers(request):  
    """Доступные предложения"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    
    projects_search_q = request.GET.get('offers_search', '').strip()
    
    
    available_projects = _get_available_projects(request)     
    total_projects = available_projects.count()
    
    available_projects_page = _paginate(request, available_projects, 6, 'projects_page')
    context = {
        "offers_search_query": projects_search_q,
        "total_projects":total_projects,
        'projects': available_projects_page,
    }
    
    return render(request, 'partner_app/dashboard/partner/offers/offers.html',context=context)