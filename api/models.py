from __future__ import unicode_literals

from django.db import models
from project.models import Project

# Create your models here.
from project.models import Project


class ApiInfo(models.Model):
    project = models.ForeignKey(Project)
    name = models.CharField(max_length=128)
    method = models.CharField(max_length=10)
    url = models.URLField()
    scene = models.CharField(max_length=128)
    description = models.CharField(max_length=128)
    overtime = models.IntegerField(default=10)
    validate_method = models.CharField(max_length=128)
    modify_recently = models.DateField()

    def __str__(self):
        return self.name


class ApiTest(models.Model):
    api_info = models.ForeignKey(ApiInfo)
    project_id = models.IntegerField(default=0)
    name = models.CharField(max_length=128)
    test_method = models.CharField(max_length=128)
    param = models.CharField(max_length=128)
    post_data = models.CharField(max_length=128)
    desc = models.CharField(max_length=128)
    task_type = models.CharField(max_length=128)
    total_run = models.IntegerField(default=0)
    success_run = models.IntegerField(default=0)
    fail_run = models.IntegerField(default=0)
    status = models.CharField(max_length=128)

    def __str__(self):
        return self.name


class ApiTestMethod(models.Model):
    api_info = models.ForeignKey(ApiInfo)
    name = models.CharField(max_length=128)
    param = models.CharField(max_length=256, null=True)
    return_value = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name


class ApiTestTaskType(models.Model):
    api_info = models.ForeignKey(ApiInfo)
    name = models.CharField(max_length=128, null=True)
    param = models.CharField(max_length=128, null=True)

    def __str__(self):
        return self.name



class CommonRequestParam(models.Model):
    api_info = models.ForeignKey(ApiInfo)
    key = models.CharField(max_length=128)
    value = models.CharField(max_length=128)
    type = models.CharField(max_length=128)
    position = models.CharField(max_length=128)
    url_encode = models.BooleanField(default=True)

    def __str__(self):
        return self.key


class Response(models.Model):
    api_info = models.ForeignKey(ApiInfo)
    body = models.CharField(max_length=2048)
    status_code = models.IntegerField(default=0)

    def __str__(self):
        return self.api_info.name


class ResponseHeader(models.Model):
    response = models.ForeignKey(Response)
    key = models.CharField(max_length=128, null=False, unique=True)
    value = models.CharField(max_length=128, null=False)

    def __str__(self):
        return self.key


class ResponseBody(models.Model):
    response = models.ForeignKey(Response)
    key = models.CharField(max_length=128, null=False)
    path = models.CharField(max_length=128, null=False, unique=True)
    type = models.CharField(max_length=128, null=False)
    type_rule = models.CharField(max_length=128,null=False)

    def __str__(self):
        return self.key


class KeyType(models.Model):
    name = models.CharField(max_length=128)
    short = models.CharField(max_length=128)
    desc = models.CharField(max_length=256)

    def __str__(self):
        return self.name


# class TypeRule(models.Model):
#     type = models.ForeignKey(KeyType)
#     rule = models.CharField(max_length=128)
#     method = models.CharField(max_length=128)
#     desc = models.CharField(max_length=256)
#
#     def __str__(self):
#         return self.rule


