from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages

from partner_app.forms import PlatformForm
from partner_app.models import Platform

@login_required
@require_POST
def add_platform(request):
    form = PlatformForm(request.POST)
    try:
        platform = form.save(commit=False)
        platform.partner = request.user
        platform.save()
        print("add platform")
        return redirect("dashboard")
    except Exception as e:
        print(e)
        messages.error(request, "Уже существует площадка с таким  URL или ID или названием.",extra_tags="platform_add_error")
        platform = PlatformForm()
        
    return redirect("dashboard")


@login_required
@require_POST
def delete_platform(request, platform_id):
    platform = Platform.objects.get(id=platform_id)
    platform.delete()
    return redirect("dashboard")