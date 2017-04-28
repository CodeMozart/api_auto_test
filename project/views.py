# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time

import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

from api.models import ApiInfo
from models import *


# Create your views here.
def view(request):

    return render(request, 'project/view.html', {'project_list': get_project_list()})


def get_project_list():

    all_item = Project.objects.all()
    project_list = []
    for item in all_item:
        project_dict = dict({})
        project_dict['id'] = item.id
        project_dict['name'] = item.name

        created_timeStamp = item.created
        created_timeArray = time.localtime(created_timeStamp)
        created_time = time.strftime("%Y-%m-%d", created_timeArray)
        project_dict['created'] = created_time
        project_dict['owner'] = item.owner
        project_list.append(project_dict)

    return project_list


def add_project(request):
    if request.method == "POST":
        try:
            data = request.POST
            created_arr = time.strptime(data.get('created'), "%Y-%m-%d")
            created_int = int(time.mktime(created_arr))
            project = Project(name=data.get('name'), created=created_int, owner=data.get('owner'))
            project.save()
            context = {'flag': 'Success', 'id': project.id}
        except Exception, e:
            context = {"flag": 'Error', "context": str(e)}

        return HttpResponse(json.dumps(context))

    return render(request, 'project/view.html', {'project_list': get_project_list()})


def delete_project(request):
    print '点击了删除按钮'
    if request.method == "POST":
        try:
            data = request.POST
            project = Project.objects.get(id=data.get('project_id'))
            project.delete()
            context = {'flag': 'Success'}
        except Exception, e:
            context = {"flag": 'Error', "context": str(e)}

        return HttpResponse(json.dumps(context))

    return render(request, 'project/view.html', {'project_list': get_project_list()})


def change_project(request):
    print '点击了完成修改按钮'
    if request.method == "POST":
        try:
            data = request.POST
            project = Project.objects.get(id=data.get('id'))
            project.name = data.get('name')
            project.owner = data.get('owner')
            project.save()
            context = {'flag': 'Success'}
        except Exception, e:
            context = {"flag": 'Error', "context": str(e)}
        return HttpResponse(json.dumps(context))
    return render(request, 'project/view.html', {'project_list': get_project_list()})


def detail(request, project_id):
    config_list = list(ProjectConfig.objects.filter(project_id=project_id).values())
    api_list = list(ApiInfo.objects.filter(project_id=project_id).values())
    context = {
        'id': project_id,
        'project_config_list': config_list,
        'api_list': api_list,
    }
    return render(request, 'project/detail.html', context)


def create_config(request):
    project_id = request.POST['project_id']
    name = request.POST['config_name']
    base_url = request.POST['base_url']
    common_params = request.POST['common_params']
    description = request.POST['description']
    config = ProjectConfig(project_id=project_id, name=name, base_url=base_url, common_params=common_params, description=description)
    config.save()
    return redirect('/project/' + project_id)


def read_config(request):
    id = request.GET['id']
    config = ProjectConfig.objects.get(id=id)
    data = {
        'id': config.id,
        'name': config.name,
        'base_url': config.base_url,
        'common_params': config.common_params,
        'description': config.description
    }
    return HttpResponse(json.dumps(data))


def update_config(request):
    project_id = request.POST['project_id']
    id = request.POST['id']
    name = request.POST['config_name']
    base_url = request.POST['base_url']
    common_params = request.POST['common_params']
    description = request.POST['description']
    config = ProjectConfig.objects.get(id=id)
    config.project_id = project_id
    config.name = name
    config.base_url = base_url
    config.common_params = common_params
    config.description = description
    config.save()
    return redirect('/project/' + project_id)


def delete_config(request):
    id = request.POST['id']
    model = ProjectConfig.objects.get(id=id)
    model.delete()

    return HttpResponse()


def create_api(request):
    project_id = request.POST['project_id']
    name = request.POST['name']
    method = request.POST['method']
    url = request.POST['url']
    scene = request.POST['scene']
    description = request.POST['description']
    overtime = request.POST['overtime']
    validate_method = request.POST['validate_method']
    modify_recently = datetime.datetime.now().strftime('%Y-%m-%d')

    api_info = ApiInfo(project_id=project_id, name=name, method=method, url=url, scene=scene, description=description,
                       overtime=overtime, validate_method=validate_method, modify_recently=modify_recently)
    api_info.save()

    return redirect('/project/' + project_id)


def read_api(request):
    id = request.GET['id']
    api = ApiInfo.objects.get(id = id)
    data = {
        'id': api.id,
        'name': api.name,
        'method': api.method,
        'url': api.url,
        'scene': api.scene,
        'description': api.description,
        'overtime': api.overtime,
        'validate_method': api.validate_method,
    }
    return HttpResponse(json.dumps(data))


def update_api(request):
    project_id = request.POST['project_id']
    id = request.POST['id']
    name = request.POST['name']
    method = request.POST['method']
    url = request.POST['url']
    scene = request.POST['scene']
    description = request.POST['description']
    overtime = request.POST['overtime']
    validate_method = request.POST['validate_method']
    modify_recently = datetime.datetime.now().strftime('%Y-%m-%d')

    api = ApiInfo.objects.get(id=id)
    api.project_id = project_id
    api.name = name
    api.method = method
    api.url = url
    api.scene = scene
    api.description = description
    api.overtime = overtime
    api.validate_method = validate_method
    api.modify_recently = modify_recently
    api.save()

    return redirect('/project/' + project_id)


def delete_api(request):
    id = request.POST['id']
    api_info = ApiInfo.objects.get(id=id)
    api_info.delete()

    return HttpResponse()