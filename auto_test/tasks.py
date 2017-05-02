from auto_test.celery import *
from task.models import TimingTask

@app.task
def api_test_time_task(taskid):
    print taskid

    timing_task = TimingTask.objects.get(id=taskid)
    api_list = timing_task.api_test_list