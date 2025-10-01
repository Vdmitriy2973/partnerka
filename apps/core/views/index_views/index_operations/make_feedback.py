from django.http import JsonResponse
from django.views.decorators.http import require_POST

from utils import send_email_via_mailru


@require_POST
def feedback(request):
    """Обратная связь с пользователями"""
    name = request.POST['name']
    mail = request.POST['mail']
    phone = request.POST.get('phone','')
    if not phone:
        phone = "Отстутствует"
    review = request.POST['review']
    review = f"""Имя:{name}
Почта: {mail}
Номер: {phone}
Текст обращения: {review}"""
    
    send_email_via_mailru.delay(recipient="vdmitriy2973@gmail.com",message=review,subject='Заявка от посетителя сайта')
    
    return JsonResponse({"success":True})
