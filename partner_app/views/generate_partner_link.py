from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import IntegrityError

from partner_app.models import ProjectPartner,PartnerLink

@login_required
@require_POST
def generate_link(request, partnership_id):
    try:
        partnership = get_object_or_404(ProjectPartner, id=partnership_id)
        
        generated_link = request.POST.get('generated_link', '').strip()
        
        # Валидация ссылки
        if not generated_link:
            messages.error(request, "Ссылка не может быть пустой",extra_tags="generate_link_error")
            return redirect('dashboard')
        
        if not generated_link.startswith(('http://', 'https://')):
            messages.error(request, "Ссылка должна начинаться с http:// или https://",extra_tags="generate_link_error")
            return redirect('dashboard')
        
        # Проверка, что ссылка уже не существует
        if PartnerLink.objects.filter(url=generated_link, partnership=partnership).exists():
            messages.error(request, "Такая ссылка уже существует",extra_tags="generate_link_error")
            return redirect('dashboard')
        
        # Создание ссылки
        partner_link = PartnerLink.objects.create(
            partner=request.user,
            project=partnership.project,
            partnership=partnership,
            url=generated_link,
        )
        
        partnership.partner_link = partner_link
        partnership.save()
        
        messages.success(request, "Партнёрская ссылка успешно сгенерирована!",extra_tags="generate_link_success")
        return redirect('dashboard')
        
    except IntegrityError:
        messages.error(request, "Ошибка базы данных при создании ссылки",extra_tags="generate_link_error")
        return redirect('dashboard')
    except Exception as e:
        # В продакшне лучше использовать логирование
        print(f"Unexpected error: {e}")
        messages.error(request, f"Произошла непредвиденная ошибка: {e}",extra_tags="generate_link_error")
        return redirect('dashboard')