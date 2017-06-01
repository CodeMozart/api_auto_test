# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-04 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setting', '0003_auto_20170428_1453'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiValidator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('desc', models.CharField(max_length=1024)),
                ('is_default', models.BooleanField(default=False)),
            ],
        ),
    ]
