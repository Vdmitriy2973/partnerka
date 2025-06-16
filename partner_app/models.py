from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('partner', 'Партнёр'),
        ('advertiser', 'Рекламодатель'),
    )
    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=20)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class PartnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    traffic_source = models.CharField(max_length=100)

class AdvertiserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    position = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100)