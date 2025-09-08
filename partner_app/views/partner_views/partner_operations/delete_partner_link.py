from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from partner_app.models import PartnerLink

@login_required
@require_POST
def delete_partner_link(request, link_id):
    partner_link = get_object_or_404(PartnerLink,id=link_id,partner=request.user)
    partner_link.delete()
    messages.success(request,message="Партнёрская ссылка успешно удалена!",extra_tags="delete_link_success")
    return redirect('partner_links')