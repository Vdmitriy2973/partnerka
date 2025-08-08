from django.db import models

class Conversion(models.Model):
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='conversions'
    )
    partner = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversions'
    )
    partner_link = models.ForeignKey(
        'PartnerLink',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversions'
    )
    platform = models.ForeignKey(
        'Platform',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='conversions'
    )
    
    partnership = models.ForeignKey(
        'ProjectPartner',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
        related_name='conversions',
        verbose_name="Сотрудничество партнёра с проектом"
    )
    order_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма конверсии'
    )
    created_at = models.DateTimeField(auto_now_add=True,)
    details = models.TextField(blank=True)

    class Meta:
        verbose_name ="Конверсия"
        verbose_name_plural ="Конверсии"
        indexes = [
            models.Index(fields=['project']),
            models.Index(fields=['partner']),
            models.Index(fields=['partnership']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Конверсия #{self.id} (Партнёр: {self.partner})"