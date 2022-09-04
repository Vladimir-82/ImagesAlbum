import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ImagesAlbum.settings')
app = Celery('ImagesAlbum')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-report-every-day': {
        'task': 'app.tasks.send_view_count_report',
        'schedule': crontab(minute=0, hour=0),
    },
}