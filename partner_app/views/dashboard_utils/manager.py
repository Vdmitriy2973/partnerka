from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth import get_user_model

from datetime import timedelta

from partner_app.models import Project, Platform
from .common import _paginate


def handle_manager_dashboard(request):
    User = get_user_model()
        
    users = User.objects.filter(user_type__in=['partner', 'advertiser']).order_by("-date_joined")
    count = 10
    users = _paginate(request,users,count,"users_page")

    new_users = User.objects.filter(
        date_joined__gte=timezone.now() - timedelta(days=1)
    ).count()


    pending_projects = Project.objects.filter(status='На модерации').order_by('-created_at')
    pending_platforms = Platform.objects.filter(status='На модерации').order_by('-created_at')
    pending_list = list(pending_projects) + list(pending_platforms)
    pending_items = _paginate(request,pending_list,count,"users_page")

    context = {
        "user":request.user,
        "users":users,
        "pending_items": pending_items,
        "pending_items_len": len(pending_list),
        "new_users_count":new_users
    }
    return render(request, "partner_app/dashboard/manager.html",context)