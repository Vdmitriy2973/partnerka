# from django.db import models
# from django.utils import timezone

# class ClickEvent(models.Model):
#     project = models.ForeignKey(
#         'Project',
#         verbose_name="ID проекта"
#     )
#     partner = models.ForeignKey(
#         'User',
#         null=True,
#         blank=True,
#         verbose_name="ID партнёра",
#         help_text="Необязательно, если клик не от партнёра"
#     )
#     session_id = models.CharField(
#         max_length=64,
#         verbose_name="ID сессии",
#         help_text="Идентификатор сессии пользователя"
#     )
#     referrer = models.URLField(null=True, blank=True,default=None, verbose_name="Источник")
#     user_agent = models.TextField(null=True, blank=True, verbose_name="User-Agent")
#     ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP-адрес")
    
#     # Даты
#     created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата клика")
    
#     class Meta:
#         verbose_name = "Клик"
#         verbose_name_plural = "Клики"
#         indexes = [
#             models.Index(fields=["project_id"]),
#             models.Index(fields=["partner_id"]),
#             models.Index(fields=["session_id"]),
#             models.Index(fields=["created_at"]),
#         ]

#     def __str__(self):
#         return f"Клик #{self.id} (Проект: {self.project_id}, Партнёр: {self.partner_id})"