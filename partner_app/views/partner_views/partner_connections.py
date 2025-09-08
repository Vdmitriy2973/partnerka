import json

from django.shortcuts import render,redirect

from .common import _get_connected_projects
from partner_app.utils import _apply_search, _paginate

def partner_connections(request):  
    """подключенные проекты"""
    user = request.user
    if not user.is_authenticated:
        return redirect('/?show_modal=auth')
    if not hasattr(request.user,"partner_profile"):
        return redirect('index')
    
    connection_search_q = request.GET.get('connections_search', '').strip()
    connected_projects = _get_connected_projects(request)
    for project in connected_projects:
        project.conversions_count_value = project.get_partner_conversion(user)
        project.conversions_percent_value = project.get_partner_conversion_percent(user)
        project.clicks_count_value = project.get_partner_clicks(user)
        project.has_link = project.has_partner_link(user)
        project.params_json = json.dumps(list(
            project.params.all().values('name', 'description', 'param_type', 'example_value')
        ))
    if connection_search_q:
        connected_projects = _apply_search(connected_projects, connection_search_q, ['name'])
    
    total_connected_projects = connected_projects.count()
    active_connected_projects = connected_projects.filter(
        partner_memberships__status="Активен"
    ).count()
    suspended_connected_projects = connected_projects.filter(
        partner_memberships__status="Приостановлен"
    ).count()
    
    connected_projects_page = _paginate(request, connected_projects, 5, 'connected_projects_page')
    context = {
        'connected_projects': connected_projects_page,
        'total_connected_projects':total_connected_projects,
        'active_connected_projects':active_connected_projects,
        'suspended_connected_projects':suspended_connected_projects
        
    }
    
    return render(request, 'partner_app/dashboard/partner/connections/connections.html',context=context)