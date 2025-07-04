from django.db import models
from .user import User
from .project import Project

class ProjectPartner(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='project_partners'
    )

    partner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='partner_projects'
    )

    joined_at = models.DateTimeField(auto_now_add=True)
    
    is_approved = models.BooleanField(
        default=False,
        help_text="Подтверждён ли доступ партнёра к проекту"
    )

    class Meta:
        unique_together = [('project', 'partner')]

    def __str__(self):
        return f"{self.partner} → {self.project}"