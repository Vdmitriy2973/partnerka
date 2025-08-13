from django.core.mail import send_mail

def send_email_via_mailru(recipient,message,subject):
    """
    Отправка писем через почту mail.ru
    
    :param recipient: Почта получателя. Пример: test_mail@gmail.com
    :param message: Отправляемое сообщение получателю
    :param subject: Тема письма
    """
    recipient_list = [recipient]
    try:
        send_mail(
            subject,
            message,
            None,  # Использует DEFAULT_FROM_EMAIL
            recipient_list,
            fail_silently=False,
        )
    except Exception as e:
        print(e)