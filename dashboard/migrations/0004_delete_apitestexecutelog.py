# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-26 13:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_apitestexecutelog'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ApiTestExecuteLog',
        ),
    ]
