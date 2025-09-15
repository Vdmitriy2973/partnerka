from django.shortcuts import render, redirect

from partner_app.utils import _paginate,_apply_search
from partner_app.models import Project,ClickEvent,Conversion,AdvertiserActivity
from partner_app.forms import ProjectForm,ProjectParamForm


def advertiser_projects(request):
    """Страница с проектами рекламодателя"""
    
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"advertiserprofile"):
        return redirect('index')
    if user.is_authenticated and user.is_currently_blocked():
        return render(request, 'account_blocked/block_info.html')
    
    notifications_count = AdvertiserActivity.objects.filter(advertiser=request.user.advertiserprofile).count()
    
    projects = Project.objects.filter(
        advertiser=request.user
    ).select_related('advertiser').order_by('-created_at')
    
    projects_search_q = request.GET.get('projects_search', '').strip()

    if projects_search_q:
        projects = _apply_search(projects, projects_search_q,['name'])
        
    projects_page = _paginate(request, projects, 6, 'projects_page')
    
    clicks_count = ClickEvent.objects.filter(advertiser=request.user.advertiserprofile).count()
    conversion_percent = 0
    conversions = Conversion.objects.filter(advertiser=request.user.advertiserprofile).select_related("project","partner").order_by("-created_at")
    conversions_count = conversions.count()
    if clicks_count > 0:
        conversion_percent =  f"{(conversions_count / clicks_count) * 100:.2f}"
    
    context = {
        "notifications_count":notifications_count,
        
        "projectForm": ProjectForm(),
        'projectParamForm':ProjectParamForm(),
        "projects": projects_page,
        "clicks_count":clicks_count,
        "conversion_percent":conversion_percent,
        "projects_search_query":projects_search_q,
    }
    return render(request, 'partner_app/dashboard/advertiser/projects/projects.html',context=context)