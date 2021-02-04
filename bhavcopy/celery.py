import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bhavcopy.settings')

app = Celery('bhavcopy')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_url = settings.CACHES['default']['LOCATION']

app.conf.beat_schedule = {
    # Execute every day at 6:00 p.m.
    'fetch-everyday': {
        'task': 'website.tasks.cache_bhavcopy',
        'schedule': crontab(minute=0, hour=18),
    },
}

app.autodiscover_tasks()
