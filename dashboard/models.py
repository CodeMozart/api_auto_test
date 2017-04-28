from __future__ import unicode_literals

from django.db import models

import datetime

# Create your models here.


class ApiTestExecuteLog(models.Model):
    project_id = models.IntegerField(default=0)
    api_id = models.IntegerField(default=0)
    execute_time = models.CharField(max_length=128)
    scheduled = models.BooleanField(default=False)
    task_id = models.IntegerField(default=0)
    execute_result = models.BooleanField(default=False)
    error_msg = models.CharField(max_length=256)
    success_data = models.TextField(max_length=None)

    def __str__(self):
        return self.execute_time
