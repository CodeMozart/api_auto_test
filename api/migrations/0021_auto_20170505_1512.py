# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-05 07:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_auto_20170503_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='response',
            name='api_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ApiInfo', unique=True),
        ),
    ]