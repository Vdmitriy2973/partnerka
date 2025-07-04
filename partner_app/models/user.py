from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('partner', 'Партнёр'),
        ('advertiser', 'Рекламодатель'),
        ('manager', 'Менеджер')
    )

    email = models.EmailField('email address', unique=True)
    user_type = models.CharField(
        'Тип пользователя',
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='partner' 
    )
    phone = models.CharField(
        'Телефон',
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        default=None
    )
    description = models.CharField(
        'Описание',
        max_length=200,
        default='',
        blank=True
    )
    email_notifications = models.BooleanField(
        'Email уведомления',
        default=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username or self.email


class PartnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    traffic_source = models.CharField(max_length=100)

class AdvertiserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    position = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)
    api_key = models.CharField(max_length=50,unique=True,blank=True,null=True, default=None)


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)