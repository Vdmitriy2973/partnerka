from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from partner_app.models import PartnerLink

@login_required
@require_POST
def delete_partner_link(request, link_id):
    partner_link = PartnerLink.objects.get(id=link_id,partner=request.user)
    partner_link.delete()
    return redirect('dashboard')