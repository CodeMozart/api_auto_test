# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-04-21 06:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_responseheader'),
    ]

    operations = [
        migrations.CreateModel(
            name='KeyType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('short', models.CharField(max_length=128)),
                ('desc', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='ResponseBody',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=128)),
                ('path', models.CharField(max_length=128, unique=True)),
                ('type', models.CharField(max_length=128)),
                ('type_rule', models.CharField(max_length=128)),
                ('max', models.IntegerField(default=0)),
                ('min', models.IntegerField(default=0)),
                ('response', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Response')),
            ],
        ),
        migrations.CreateModel(
            name='TypeRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rule', models.CharField(max_length=128)),
                ('method', models.CharField(max_length=128)),
                ('desc', models.CharField(max_length=256)),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.KeyType')),
            ],
        ),
    ]
