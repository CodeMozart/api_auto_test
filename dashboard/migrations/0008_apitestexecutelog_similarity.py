# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-04 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_apitestexecutelog_test_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='apitestexecutelog',
            name='similarity',
            field=models.FloatField(default=0),
        ),
    ]
