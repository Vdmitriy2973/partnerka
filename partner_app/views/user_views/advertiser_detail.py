from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from partner_app.models import User
from django.core.paginator import Paginator

@login_required
def advertiser_detail(request, advertiser_id):
    advertiser = get_object_or_404(
        User,id=advertiser_id
    )
    
    # Проверка прав доступа
    if not hasattr(advertiser, 'advertiserprofile'): 
        messages.error(request, message="Этот пользователь не является рекламодателем")
        if hasattr(request.user, 'advertiserprofile'): 
            return redirect('advertiser_dashboard')
        return redirect('dashboard')
    count = 6
    projects = advertiser.managed_projects.all()
    project_paginator = Paginator(projects, count)
    project_page_number = request.GET.get('projects_page')
    project_page_obj = project_paginator.get_page(project_page_number)

    context = {
        'advertiser': advertiser,
        'projects': project_page_obj
    }
    return render(request, 'partner_app/advertisers/advertiser_details.html', context)