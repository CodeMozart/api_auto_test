from __future__ import absolute_import, unicode_literals
import os
import time
from celery import Celery
# from test_executor.test_executor import TimeTaskExecutor
# from api.models import *

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'auto_test.settings')

app = Celery('auto_test')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
    return self


@app.task
def add(x, y):
    time.sleep(5)
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)




# @app.task
# def execute_time_task(taskid):
#     time_task_executor = TimeTaskExecutor(taskid=taskid)
#     time_task_executor()
#     print 'aaa'