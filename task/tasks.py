from auto_test.celery import *
from test_executor.test_executor import *
from task.models import *


@app.task
def api_test_time_task(task_id):
    print 'task_id: ' + str(task_id)

    timing_task = TimingTask.objects.get(id=task_id)
    api_test_list = timing_task.api_test_list
    print 'api_test_list: ' + api_test_list

    if len(api_test_list) > 0:
        api_test_id_list = [x for x in api_test_list.split(',')]
        for api_test_id in api_test_id_list:
            execute_validate.delay(api_test_id, task_id)



@app.task
def execute_validate(test_id, task_id):

    test_executor = TestExecutor(test_id=test_id, task_id=task_id)
    print 'result: ' + str(test_executor.send_request().get('status'))
