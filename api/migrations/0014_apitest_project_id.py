# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-25 03:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_auto_20170424_1127'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitest',
            name='project_id',
            field=models.IntegerField(default=0),
        ),
    ]