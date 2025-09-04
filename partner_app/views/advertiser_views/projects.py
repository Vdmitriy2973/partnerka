from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from partner_app.utils import _paginate,_apply_search
from partner_app.models import Project,ClickEvent,Conversion
from partner_app.forms import ProjectForm,ProjectParamForm

@login_required
def advertiser_projects(request):
    """Страница с проектами рекламодателя"""
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
        "projectForm": ProjectForm(),
        'projectParamForm':ProjectParamForm(),
        "projects": projects_page,
        "clicks_count":clicks_count,
        "conversion_percent":conversion_percent,
        "projects_search_query":projects_search_q,
    }
    return render(request, 'partner_app/dashboard/advertiser/projects/projects.html',context=context)