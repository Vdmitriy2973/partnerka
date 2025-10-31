from django.db import models
from django.core.validators import MinValueValidator

class PartnerProfile(models.Model):
    user = models.OneToOneField(
        'users.User', 
        on_delete=models.CASCADE,
        related_name='partner_profile',
        verbose_name='Пользователь'
    )
    balance = models.DecimalField(
        verbose_name="Баланс",
        decimal_places=2,
        default=0.00, 
        max_digits=10,
        validators=[MinValueValidator(0.00)],
    )

    @property 
    def conversions_percent(self):
        if self.clicks.count() == 0:
            return 0.0
        return f"{(self.conversions.count() / self.clicks.count()) * 100:.2f}"
    
    @property
    def conversions_count(self):
        return self.conversions.count()

    @property
    def clicks_count(self):
        return self.clicks.count() 
    
    class Meta:
        verbose_name = 'Партнёр'
        verbose_name_plural = 'Партнёры'

    def __str__(self):
        return f"Профиль: {self.user.username}" if self.user else "Непривязанный профиль"
