# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-25 08:15
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_apitest_project_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typerule',
            name='type',
        ),
        migrations.DeleteModel(
            name='TypeRule',
        ),
    ]