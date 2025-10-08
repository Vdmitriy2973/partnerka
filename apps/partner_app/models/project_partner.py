from django.conf import settings
from django.db import models

class ProjectPartner(models.Model):
    """Основная модель партнёрства"""
    class StatusType(models.TextChoices):
        ACTIVE = 'Активен', 'Активен'
        SUSPENDED = 'Приостановлен', 'Приостановлен'
        BLOCKED = 'Заблокировано', 'Заблокировано'

    partner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='+',
        verbose_name='Партнёр'
    )
    
    advertiser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="+",
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
    
    joined_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name='Дата начала сотрудничества'
    )
    
    suspension_reason = models.TextField(
        max_length=50,
        verbose_name="Причина приостановления сотрудничества",
        help_text="Например: Тех. работы",
        blank=True,
        null=True,
        default=None
    )
    suspension_comment = models.TextField(
        max_length=300,
        verbose_name="Доп. комментарий к приостановке сотрудничества",
        blank=True,
        null=True,
        default=None
    )

    class Meta:
        unique_together = ('project', 'partner')
        verbose_name = 'Партнёрство в проекте'
        verbose_name_plural = 'Партнёрства в проектах'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.partner} → {self.project} ({self.get_status_display()})"