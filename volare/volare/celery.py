import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'volare.settings')

app = Celery('volare')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'cancel-expired-reservations-every-1-minute': {
        'task': 'bookings.tasks.cancel_expired_reservations',
        'schedule': crontab(minute='*/1'),  # every 1 minute
    },
}