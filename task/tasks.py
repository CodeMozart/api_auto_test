from auto_test.celery import *
from test_executor.test_executor import TimeTaskExecutor

@app.task
def api_test_time_task(taskid):
    print taskid
