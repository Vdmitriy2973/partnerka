import os
import platform
from celery import Celery

# Определяем ОС
IS_WINDOWS = platform.system().lower() == 'windows'

# Установите переменную окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_partner_project.settings')

app = Celery('website_partner_project')

# Загрузка настроек из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

app.conf.worker_max_tasks_per_child = 1000
app.conf.worker_max_memory_per_child = 400000  # 400MB