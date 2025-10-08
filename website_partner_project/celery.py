import os
from celery import Celery



os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'website_partner_project.settings')

app = Celery('website_partner_project')


app.config_from_object('django.conf:settings', namespace='CELERY')


app.autodiscover_tasks()

app.conf.worker_max_tasks_per_child = 1000
app.conf.worker_max_memory_per_child = 400000