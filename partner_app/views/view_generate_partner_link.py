from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from partner_app.models import ProjectPartner,PartnerLink

@login_required
@require_POST
def generate_link(request, partnership_id):
    partnership = ProjectPartner.objects.get(id=partnership_id)
    if not partnership:
        print("not found")
        return redirect('dashboard')
    partner_link = PartnerLink.objects.create(
        partner=request.user,
        project=partnership.project,
        partnership=partnership,
        url=request.POST.get('generated_link',''),
        
    )
    partnership.partner_link = partner_link
    partnership.save()
    return redirect('dashboard')