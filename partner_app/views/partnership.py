from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.views.decorators.http import require_POST
from partner_app.models import ProjectPartner,User
from partner_app.utils import send_email_via_mailru
from django.utils.timezone import now

@login_required
@require_POST
@transaction.atomic
def stop_partnership_with_partner(request,partner_id):
    """Остановить сотрудничество рекламодателя с партнёром (Со всеми подключенными проектами)"""
    
    partnership = ProjectPartner.objects.filter(
        advertiser=request.user,
        partner=partner_id
    )
    user = User.objects.get(id=partner_id)
    partnership.delete()
    date_str = now().strftime("%d.%m.%Y %H:%M")
    
    title = ""
    message = f"""Здравствуйте,{user.get_full_name()}!\n\n
Рекламодатель {request.user.get_full_name()} прекратил сотрудничество с вами {date_str}.\n\n\n
С уважением,\nКоманда поддержки"""
    send_email_via_mailru(user.email,message,"❌ Остановка сотрудничества")
    return redirect('dashboard')

@login_required
@require_POST
@transaction.atomic
def stop_partnership_with_project(request,project_id):
    """Остановить сотрудничество партнёра с проектом рекламодателя"""
    partnership = ProjectPartner.objects.get(partner=request.user,project=project_id)
    partnership.delete()
    
    title = '❌ Остановка сотрудничества'
    message = f"""Уважаемый рекламодатель,
Сообщаем вам, что партнёр {partnership.partner.get_full_name()} {partnership.partner.email} прекратил сотрудничество по проекту «{partnership.project.name}»
Причина: {request.POST.get('suspension_reason', "Не указана")}
Комментарий: {request.POST.get('suspension_comment', "Не указан")}
**Что это значит:**  
- Все ссылки партнёра деактивированы  
- Новые переходы с его ресурсов не учитываются  
- Статистика доступна в личном кабинете  

Это письмо отправлено автоматически."""    

    send_email_via_mailru(partnership.advertiser.email,message,title)
    return redirect('dashboard')

@login_required
@require_POST
def suspend_partnership(request,project_id):
    """Приостановить сотрудничество партнёра с проектом рекламодателя"""
    partnership = ProjectPartner.objects.get(partner=request.user,project=project_id)
    partnership.status = "Приостановлен"
    partnership.suspension_reason = request.POST.get('suspension_reason',None)
    partnership.suspension_comment = request.POST.get('suspension_comment',None)
    partnership.save()
    
    title = '❌ Приостановление сотрудничества'
    message = f"""Уважаемый рекламодатель,
Сообщаем вам, что партнёр {partnership.partner.get_full_name()} {partnership.partner.email} временно прекратил сотрудничество по проекту «{partnership.project.name}» временно приостановлено.
Причина: {request.POST.get('suspension_reason',"Не указана")}
Комментарий: {request.POST.get('suspension_comment',"Не указан")}

В период приостановки:
- Новые клики/конверсии не будут учитываться
- Доступ к статистике сохранится в режиме просмотра

Это письмо отправлено автоматически."""
    
    send_email_via_mailru(partnership.advertiser.email,message,title)
    return redirect('dashboard')


@login_required
@require_POST
def resume_partnership(request,project_id):
    """ Воозобновить сотрудничество партнёра с проектом рекламодателя"""
    partnership = ProjectPartner.objects.get(partner=request.user,project=project_id)
    partnership.status = "Активен"
    partnership.suspension_reason = None 
    partnership.suspension_comment = None
    partnership.save()
    
    title = f'✅ Возобновление сотрудничества'
    message = f"""Партнёр {partnership.partner.get_full_name()} снова продвигает ваш проект «{partnership.project.name}».  

После возобновления сотрудничества у вас будут учитываться конверсии/переходы.
Это письмо отправлено автоматически."""
    send_email_via_mailru(partnership.advertiser.email,message,title)
    
    return redirect('dashboard')