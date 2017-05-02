# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=30)
    created = models.IntegerField()
    owner = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class ProjectConfig(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    base_url = models.CharField(max_length=128)
    common_params = models.CharField(max_length=128)
    description = models.CharField(max_length=128)

    def __str__(self):
        return self.name
