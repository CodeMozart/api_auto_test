# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-04 09:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0005_auto_20170428_1545'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timingtask',
            name='run_time',
        ),
    ]