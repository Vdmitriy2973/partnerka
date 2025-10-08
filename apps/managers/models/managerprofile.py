from django.db import models

class ManagerProfile(models.Model):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = 'Менеджер'
        verbose_name_plural = 'Менеджеры'

    def __str__(self):
        return f"Профиль: {self.user.username}" if self.user else "Непривязанный профиль"