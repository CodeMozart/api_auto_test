# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render, redirect

from setting.models import CustomValidateRule


def custom_validator(request):
    cvr = list(CustomValidateRule.objects.all().values())
    context = {
        'cvr_list': cvr
    }
    return render(request, 'setting/custom_validator.html', context)


def create_custom_validator(request):
    name = request.POST.get('name')
    code = request.POST.get('code')

    model = CustomValidateRule(name=name,code=code)
    model.save()
    return redirect('/setting/custom-validator')


def read_custom_validator(request):
    id = request.GET.get('id')
    model = CustomValidateRule.objects.get(id=id)
    data = {
        'id': model.id,
        'name': model.name,
        'code': model.code
    }
    return HttpResponse(json.dumps(data))


def update_custom_validator(request):
    id = request.POST.get('id')
    name = request.POST.get('name')
    code = request.POST.get('code')
    model = CustomValidateRule.objects.get(id=id)
    model.name = name
    model.code = code
    model.save()

    return redirect('/setting/custom-validator')


def delete_custom_validator(request):
    id = request.POST.get('id')
    model = CustomValidateRule.objects.get(id=id)
    model.delete()

    return HttpResponse()
