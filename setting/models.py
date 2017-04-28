# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class CustomValidateRule(models.Model):
    name = models.CharField(max_length=128, unique=True)
    code = models.TextField()
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name