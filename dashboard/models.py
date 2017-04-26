from __future__ import unicode_literals

from django.db import models

# Create your models here.


class ApiTestExecuteLog(models.Model):
    project_id = models.IntegerField
    api_id = models.IntegerField
    execute_time = models.CharField(max_length=128)
    scheduled = models.BooleanField(default=False)
    task_id = models.IntegerField
    execute_result = models.BooleanField(default=False)
    error_msg = models.CharField(max_length=256)
    success_data = models.TextField


