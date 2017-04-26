from __future__ import unicode_literals

from django.db import models

# Create your models here.


class TimingTask(models.Model):
    name = models.CharField(max_length=30)
    type = models.IntegerField()
    between_time = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    global_value = models.CharField(max_length=128)
    state = models.IntegerField()
    api_test_list = models.TextField(default='')
