from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.conf import settings 

class AdvertiserTransaction(models.Model):
    # Варианты для способа выплаты
    PAYMENT_METHOD_CHOICES = [
        ('wallet', 'Электронный кошелёк'),
        ('card', 'Банковская карта'),
        ('bank_transfer', 'Банковский перевод'),
        ('sbp', 'Система быстрых платежей (СБП)'),
    ]
    
    class STATUS_CHOICES(models.TextChoices):
        PENDING = 'В обработке'
        PROCCESSED = 'Обработано'
        COMPLETED = 'Пополнено'
        REJECTED = 'Отменено'

    advertiser = models.ForeignKey(
        'AdvertiserProfile',
        related_name='transactions',
        verbose_name='Получатель',
        on_delete=models.CASCADE
    )
    
    # Основные поля
    date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name='Дата транзакции'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(300)],
        verbose_name='Сумма'
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='card',
        verbose_name='Способ пополнения'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='В обработке',
        verbose_name='Статус транзакции'
    )

    rejection_reason = models.TextField(
        blank=True,
        null=True,
        verbose_name='Причина отклонения',
        help_text='Укажите причину, если транзакция отклонена'
    )
    
    def get_amount_with_commission(self):
        return self.amount-((self.amount / 100) * Decimal(settings.PARTNER_PAYOUT_SETTINGS["fee_percent"]))
    
    def clean(self):
        """
        Проверяет, что причина отклонения заполнена при статусе REJECTED.
        """
        if self.status == AdvertiserTransaction.STATUS_CHOICES.REJECTED and not self.rejection_reason:
            raise ValidationError(
                {'rejection_reason': 'Причина отклонения обязательна для статуса "Отменено".'}
            )
        if self.status != AdvertiserTransaction.STATUS_CHOICES.REJECTED and self.rejection_reason:
            self.rejection_reason = None

    class Meta:
        verbose_name = 'Пополнение'
        verbose_name_plural = 'Пополнения'
        ordering = ['-date']
        
    def __str__(self):
        return f'Пополнение #{self.id} - {self.amount} ({self.status})'