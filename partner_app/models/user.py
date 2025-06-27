from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('partner', 'Партнёр'),
        ('advertiser', 'Рекламодатель'),
        ('manager','Менеджер')
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20)
    description = models.CharField(max_length=200,default="Описание")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class NotificationSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_settings')
    
    # Настройки уведомлений
    email_notifications = models.BooleanField(default=False, verbose_name='Email уведомления')
    # sms_notifications = models.BooleanField(default=False, verbose_name='SMS уведомления')
    # sales_notifications = models.BooleanField(default=False, verbose_name='Уведомления о продажах')
    # weekly_reports = models.BooleanField(default=False, verbose_name='Еженедельные отчеты')
    # program_news = models.BooleanField(default=False, verbose_name='Новости программы')
    
    class Meta:
        verbose_name = 'Настройка уведомлений'
        verbose_name_plural = 'Настройки уведомлений'

    def __str__(self):
        return f'Настройки уведомлений для {self.user.username}'

class PartnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    traffic_source = models.CharField(max_length=100)

class AdvertiserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    position = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)