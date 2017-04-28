from auto_test.celery import *


@app.task
def api_test_time_task(taskid):
    print taskid