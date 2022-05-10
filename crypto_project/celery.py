import os
import django.conf
from celery import Celery
from celery.schedules import crontab

# import crypto_app.tasks
import crypto_project

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'crypto_project.settings')

app = Celery('crypto_project')
app.config_from_object('django.conf.settings', namespace='CELERY')
app.autodiscover_tasks()


app.conf.beat_schedule = {
    # список тасков
    'db_filling_every_minute': {
        # путь к нашему таск(функции)
        'task': 'crypto_app.tasks.db_filling',
        # crontab - периодичность
        'schedule': crontab(minute='*/1'),
    },
}





