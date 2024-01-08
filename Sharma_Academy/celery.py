import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sharma_Academy.settings')

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")
# settings.setup()

app = Celery('Sharma_Academy')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.

# app.conf.enable_utc = False

# app.conf.update(timezone = 'Asia/Kolkata')

app.autodiscover_tasks()


# @app.task(bind=True, ignore_result=True)
# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# from celery.schedules import crontab

# app.conf.beat_schedule = {
#         'every-10-seconds':{
#         'task':'users.tasks.clear_session_cache',
#         # 'schedule':10,
#         'schedule':crontab(minute='*/1'),
#         'args':('1111',)
#     }
# }