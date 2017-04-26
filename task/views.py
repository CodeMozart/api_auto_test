# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
import time
import datetime
from django.http import HttpResponse, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

from models import *
from api.models import ApiInfo, ApiTest
from project.models import Project


# Create your views here.
def view(request):
    return render(request, 'task/view.html', {'tasklist': get_task_list()})


def get_task_list():
    task_list = []
    for task in TimingTask.objects.all():
        task_dict = dict({})
        start_timeStamp = task.start_time
        start_timeArray = time.localtime(start_timeStamp)
        start_time = time.strftime("%Y-%m-%d %H:%M:%S", start_timeArray)
        end_timeStamp = task.end_time
        end_timeArray = time.localtime(end_timeStamp)
        end_time = time.strftime("%Y-%m-%d %H:%M:%S", end_timeArray)
        test = task.between_time

        if task.between_time >= 60 * 60 * 24 * 7:
            thetime = test / (60 * 60 * 24 * 7)
            between_time = '%d' % thetime + '周'
        elif task.between_time >= 60 * 60 * 24:
            thetime = test / (60 * 60 * 24)
            between_time = '%d' % thetime + '天'
        elif task.between_time >= 60 * 60:
            thetime = test / (60 * 60)
            between_time = '%d' % thetime + '小时'
        elif task.between_time >= 60:
            thetime = test / 60
            between_time = '%d' % thetime + '分钟'
        else:
            between_time = '%d' % test + '秒'

        task_dict['id'] = task.id
        task_dict['name'] = task.name
        task_dict['type'] = task.type
        task_dict['between_time'] = between_time
        task_dict['start_time'] = start_time
        task_dict['end_time'] = end_time
        task_dict['global_value'] = task.global_value
        task_dict['state'] = task.state
        task_list.append(task_dict)

    return task_list


def add_task(request):
    if request.method == "POST":
        try:
            data = request.POST
            type_data = 1 if data.get('input_type') == '定时' else 2
            state_data = 1 if data.get('input_state') == '开启' else 2
            between_time = int(data.get('input_between'))
            if data.get('input_between_unit') == '分钟':
                between_time *= 60
            elif data.get('input_between_unit') == '小时':
                between_time = between_time * 60 * 60
            elif data.get('input_between_unit') == '天':
                between_time = between_time * 60 * 60 * 24
            elif data.get('input_between_unit') == '周':
                between_time = between_time * 60 * 60 * 24 * 7

            starttime_arr = time.strptime(data.get('input_starttime'), "%Y-%m-%d %H:%M:%S")
            starttime_int = int(time.mktime(starttime_arr))
            endtime_arr = time.strptime(data.get('input_endtime'), "%Y-%m-%d %H:%M:%S")
            endtime_int = int(time.mktime(endtime_arr))

            if data.get('input_task_id'):
                task = TimingTask.objects.get(id=data.get('input_task_id'))
                task.name = data.get('input_name')
                task.type = type_data
                task.between_time = between_time
                task.start_time = starttime_int
                task.end_time = endtime_int
                task.global_value = data.get('input_global_value')
                task.state = state_data
                task.save()
            else:
                task = TimingTask(name=data.get('input_name'), type=type_data,
                                  between_time=between_time,
                                  start_time=starttime_int, end_time=endtime_int,
                                  global_value=data.get('input_global_value'), state=state_data)
                task.save()
            context = {'flag': 'Success'}
        except Exception, e:
            context = {"flag": 'Error', "context": str(e)}
    return redirect('/task/')


def delete_task(request):
    print '点击了删除按钮'
    if request.method == "POST":
        try:
            data = request.POST
            task = TimingTask.objects.get(id=data.get('task_id'))
            task.delete()
            context = {'flag': 'Success'}
        except Exception, e:
            context = {"flag": 'Error', "context": str(e)}

        return HttpResponse(json.dumps(context))

    return render(request, 'task/view.html', {'task_list': get_task_list()})


def task_detail(request):
    data = request.GET
    task = TimingTask.objects.get(id=data.get('task_id'))
    api_test_list = [x for x in task.api_test_list.split(',')]
    if len(api_test_list) < 1:
        api_test_list = api_test_list
    else:
        if api_test_list[0] == '':
            api_test_list = []
    project_list = Project.objects.all()
    for api_test in api_test_list:
        project_id = api_test.get('project_id')
        api_test['project_name'] = Project.objects.get(id=project_id).get('project_name')
        api_test['api_name'] = ApiInfo.objects.get(id=api_test.api_info)

    return render(request, 'task/detail.html',
                  {'api_test_list': api_test_list,
                   'task': task,
                   'project_list': project_list})


def add_api_test(request):
    data = request.POST
    task_id = data.get('input_task_id')
    api_test_id = data.get('input_api_test')
    task = TimingTask.objects.get(id=task_id)
    api_test_id_list = [int(x) for x in task.api_test_list.split(',')]
    if api_test_id not in api_test_id_list:
        api_test_id_list.append(api_test_id)
        str_api_test_list = ','.join(api_test_id_list)
        task.api_test_list = str_api_test_list
        task.save()

    return redirect('/task/detail?task_id=' + task_id)


def delete_api_test(request):
    print '点击了删除按钮'
    if request.method == "POST":
        try:
            data = request.POST
            task_id = data.get('task_id')
            api_test_id = data.get('api_test_id')
            task = TimingTask.objects.get(id=task_id)
            api_test_id_list = [int(x) for x in task.api_test_list.split(',')]
            if api_test_id in api_test_id_list:
                api_test_id_list.remove(api_test_id)
                str_api_test_list = ','.join(api_test_id_list)
                task.api_test_list = str_api_test_list
                task.save()

                context = {'flag': 'Success'}
            else:
                context = {"flag": 'Error', "context": '未找到此用例'}
        except Exception, e:
            context = {"flag": 'Error', "context": str(e)}

        return HttpResponse(json.dumps(context))

    return render(request, 'task/detail.html', {'task_list': get_task_list()})


def change_select_project(request):
    try:
        data = request.POST
        project_id = data.get('project_id')
        api_list = ApiInfo.objects.filter(project_id=project_id)
        need_list = []
        for api in api_list:
            need_api = dict({})
            need_api['name'] = api.name
            need_api['id'] = api.id
            need_list.append(need_api)

        context = {'flag': 'Success', 'api_list': need_list}

    except Exception, e:
        context = {"flag": 'Error', "context": str(e)}
    return HttpResponse(json.dumps(context))


def change_select_api(request):
    try:
        data = request.POST
        api_id = data.get('api_id')
        api_test_list = ApiTest.objects.filter(api_info=api_id)
        need_list = []
        for api_test in api_test_list:
            need_api_test = dict({})
            need_api_test['name'] = api_test.name
            need_api_test['id'] = api_test.id
            need_list.append(need_api_test)

        context = {'flag': 'Success', 'api_test_list': need_list}
    except Exception, e:
        context = {"flag": 'Error', "context": str(e)}

    return HttpResponse(json.dumps(context))


# 计算皮尔逊相关度：
def pearson(p, q):
    # 只计算两者共同有的
    same = 0
    for i in p:
        if i in q:
            same += 1

    n = same
    # 分别求p，q的和
    sumx = sum([p[i] for i in range(n)])
    sumy = sum([q[i] for i in range(n)])
    # 分别求出p，q的平方和
    sumxsq = sum([p[i] ** 2 for i in range(n)])
    sumysq = sum([q[i] ** 2 for i in range(n)])
    # 求出p，q的乘积和
    sumxy = sum([p[i] * q[i] for i in range(n)])
    # print sumxy
    # 求出pearson相关系数
    up = sumxy - sumx * sumy / n
    down = ((sumxsq - pow(sumxsq, 2) / n) * (sumysq - pow(sumysq, 2) / n)) ** .5
    # 若down为零则不能计算，return 0
    if down == 0:
        return 0
    r = up / down
    return r
