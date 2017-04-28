from __future__ import unicode_literals

from django.db import models

# Create your models here.


class TimingTask(models.Model):
    name = models.CharField(max_length=30, unique=True)
    type = models.IntegerField()
    run_time = models.CharField(max_length=30)
    between_time = models.IntegerField()
    start_time = models.IntegerField()
    end_time = models.IntegerField()
    global_value = models.CharField(max_length=128)
    state = models.IntegerField()
    api_test_list = models.TextField(default='')

    minute = models.CharField(max_length=64, default='*')
    hour = models.CharField(max_length=64, default='*')
    day_of_week = models.CharField(max_length=64, default='*')
    day_of_month = models.CharField(max_length=64, default='*')
    month_of_year = models.CharField(max_length=64, default='*')
