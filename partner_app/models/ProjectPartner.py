from django.db import models
from .user import User
from .project import Project

class ProjectPartner(models.Model):
    class StatusType(models.TextChoices):
        ACTIVE = 'Активен'
        SUSPENDED = 'Приостановлен'
        BLOCKED = 'Заблокировано'

    partner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='project_memberships'  
    )

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='partner_memberships'
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    
    status = models.CharField(
        max_length=20,
        default=StatusType.ACTIVE,
        choices=StatusType.choices,
        verbose_name='Статус взаимодействия',
        help_text="Подтверждён ли доступ партнёра к проекту"
    )

    custom_commission = models.DecimalField(
        null=True, 
        blank=True,
        decimal_places=2, 
        max_digits=10,
        verbose_name='Индивидуальная комиссия'
    )

    class Meta:
        unique_together = [('project', 'partner')]
        verbose_name = 'Участник проекта'
        verbose_name_plural = 'Участники проектов'

    def __str__(self):
        return f"{self.partner} → {self.project}"
