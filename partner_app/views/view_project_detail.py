from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count,Sum
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from partner_app.models import ProjectPartner,Project

@login_required
def project_detail(request, project_id):
    # Основная информация о проекте
    try:
        # Проект
        project = Project.objects.get(id=project_id)

        # Получаем статистику по партнёрам проекта
        partnership_stats = ProjectPartner.objects.filter(project=project).select_related('partner').order_by('-joined_at')

        # Пагинация
        paginator = Paginator(partnership_stats, 5)
        page_number = request.GET.get('page')
        partnerships = paginator.get_page(page_number)
        
        # Общая статистика по проекту
        total_partners = partnership_stats.count()
        active_partners = partnership_stats.filter(status=ProjectPartner.StatusType.ACTIVE).count()
        
        return render(request, 'partner_app/projects/project_details.html', {
            'project': project,
            'partnerships': partnerships,
            'total_partners': total_partners,
            'active_partners': active_partners
        })

    except Exception as e:
        # Логирование ошибки (можно настроить логирование)
        print(f"Error in project_detail: {e}")
        messages.error(request, "Произошла ошибка при загрузке страницы проекта")
        return redirect('dashboard')  # Перенаправление на главную