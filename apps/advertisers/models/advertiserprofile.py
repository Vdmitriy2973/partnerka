from django.db import models
from django.core.validators import MinValueValidator

class AdvertiserProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    api_key = models.CharField(max_length=50,unique=True,blank=True,null=True, default=None,verbose_name="API-ключ")
    balance = models.DecimalField (
        verbose_name="Мин. выплата",
        decimal_places=2,
        default=0.00, 
        max_digits=10,
        validators=[
            MinValueValidator(0.00),
        ],
    )
    
    class Meta:
        verbose_name = 'Рекламодатель'
        verbose_name_plural = 'Рекламодатели'

    def __str__(self):
        return f"Профиль: {self.user.username}" if self.user else "Непривязанный профиль"
