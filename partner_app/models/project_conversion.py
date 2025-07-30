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
    order_id = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма заказа'
    )
    created_at = models.DateTimeField(auto_now_add=True,)
    meta = models.TextField(blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['order_id']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"Конверсия #{self} (Партнёр: {self.partner})"