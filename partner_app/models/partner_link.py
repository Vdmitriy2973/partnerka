from django.db import models
from django.core.validators import URLValidator


class PartnerLink(models.Model):
    """
    Модель для хранения сгенерированных партнёрских ссылок
    """

    # Основные поля
    partner = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='partner_links',
        verbose_name='Партнёр'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='project_links',
        verbose_name='Проект'
    )
    
    partnership = models.ForeignKey(
        'ProjectPartner',
        on_delete=models.CASCADE,
        default=None,
        related_name='partner_links',
        verbose_name="Сотрудничество партнёра с проектом"
    )
    
    url = models.URLField(
        max_length=512,
        validators=[URLValidator()],
        verbose_name='Сгенерированная ссылка'
    )
        
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активна'
    )
    
    income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Доход',
        default=0
    )

    class Meta:
        verbose_name = 'Партнёрская ссылка'
        verbose_name_plural = 'Партнёрские ссылки'
        indexes = [
            models.Index(fields=['partner', 'is_active']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f'Ссылка #{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def increment_clicks(self):
        """Увеличение счётчика кликов атомарно"""
        self.clicks = models.F('clicks') + 1
        self.save(update_fields=['clicks'])
        
        
    @property 
    def conversion_percent(self):
        if self.clicks.count() == 0:
            return 0.0
        return (self.conversions.count() / self.clicks.count()) * 100