from auto_test.celery import *
from test_executor.test_executor import TimeTaskExecutor


@app.task
def api_test_time_task(task_id):
    print task_id
    print '+++++++++++++++'
    time_task_executor = TimeTaskExecutor(task_id=task_id)
    time_task_executor()


if __name__ == 'main':
    api_test_time_task(11)
