import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.setting.settings')
app = Celery('config', backend='redis')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
