from celery import shared_task
from django.core.mail import EmailMessage


@shared_task
def send_email_via_mailru(recipient, message, subject):
    try:
        
        email = EmailMessage(
            subject=subject,
            body=message,
            to=[recipient],
        )
        email.send(fail_silently=False)
            
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")
        
        

def send_email_via_mailru_with_attachment(recipient, message, subject, attachments=None):
    try:
        
        email = EmailMessage(
            subject=subject,
            body=message,
            to=[recipient],
        )
        
        successful_attachments = 0
        if attachments:
            for attachment_data in attachments:
                try:
                    filename = attachment_data.get('filename', 'file.bin')
                    file_content = attachment_data.get('content', b'')
                    content_type = attachment_data.get('content_type', 'application/octet-stream')
                    
                    # Проверяем, что content - bytes
                    if isinstance(file_content, str):
                        file_content = file_content.encode('utf-8')
                    
                    # Прикрепляем файл
                    email.attach(filename, file_content, content_type)
                    successful_attachments += 1
                    
                except Exception as e:
                    continue
        
        # Отправляем email
        email.send(fail_silently=False)
        return True
            
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")