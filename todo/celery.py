# import os
# from celery import Celery

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

# app = Celery('todo')
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()


from __future__ import absolute_import, unicode_literals

from celery import Celery
from datetime import datetime, timedelta

import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'todo.settings')

app = Celery('todo')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_emails-every-5-seconds': {
        'task': 'tasks.tasks.send_emails',
        'schedule': timedelta(seconds=5),
    }
}

app.conf.timezone = 'UTC'

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))