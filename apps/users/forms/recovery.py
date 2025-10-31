from django.contrib.auth.forms import PasswordResetForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

class HTMLPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        """
        Отправка HTML письма с правильным Content-Type
        """
        subject = "Восстановление пароля"
        
        
        html_content = render_to_string(email_template_name, context)
        
        
        text_content = strip_tags(html_content)
        
        # Создаем письмо
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=from_email,
            to=[to_email]
        )
        
        # Явно указываем HTML контент
        email.attach_alternative(html_content, "text/html")
        email.content_subtype = 'html'
        
        return email.send()
    
    def save(self, *args, **kwargs):
        if self.request:
            self.request.session['reset_requested'] = True
        return super().save(*args, **kwargs)