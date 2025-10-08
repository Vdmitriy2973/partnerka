from django.db import models
from django.utils.translation import gettext_lazy as _
class PartnerActivity(models.Model):
    class ActivityType(models.TextChoices):
        SALE = 'sale', _('Новая продажа')
        APPROVE = 'approve', _('Одобрение')
        REJECT = 'reject', _('Отклонение')
        CLICKS = 'clicks', _('Переходы по ссылке')
        PAYOUT = 'payout', _('Выплата')
        SYSTEM = 'system', _('Системное уведомление')

    partner = models.ForeignKey(
        'partners.PartnerProfile',
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name=_('Партнёр')
    )
    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        verbose_name=_('Тип активности')
    )
    title = models.CharField(
        max_length=100,
        verbose_name=_('Заголовок')
    )
    details = models.CharField(
        max_length=255,
        blank=True,
        verbose_name=_('Детали')
    )
    is_read = models.BooleanField(
        default=False,
        verbose_name=_('Прочитано')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания')
    )

    class Meta:
        verbose_name = _('Активность партнёра')
        verbose_name_plural = _('Активности партнёров')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['partner', 'is_read']),
        ]

    def __str__(self):
        return f"{self.title} - {self.partner}"