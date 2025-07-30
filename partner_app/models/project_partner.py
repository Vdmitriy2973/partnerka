from django.db import models

class ProjectPartner(models.Model):
    """Основная модель партнёрства"""
    class StatusType(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        SUSPENDED = 'Приостановлен', 'Приостановлен'
        BLOCKED = 'Заблокировано', 'Заблокировано'

    partner = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name='project_memberships',
        verbose_name='Партнёр'
    )
    advertiser = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="project_owner",
        null=True,
        blank=True,
        verbose_name='Рекламодатель'
    )
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='partner_memberships',
        verbose_name='Проект'
    )
    status = models.CharField(
        max_length=20,
        choices=StatusType.choices,
        default=StatusType.ACTIVE,
        verbose_name='Статус сотрудничества'
    )
    custom_commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name='Комиссия партнёра'
    )
    
    joined_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Дата начала сотрудничества'
    )

    class Meta:
        unique_together = ('project', 'partner')
        verbose_name = 'Партнёрство в проекте'
        verbose_name_plural = 'Партнёрства в проектах'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.partner} → {self.project} ({self.get_status_display()})"