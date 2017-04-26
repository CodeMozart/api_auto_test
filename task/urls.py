# __author__ = ''
# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.view),
    url(r'^add_task$', views.add_task),
    url(r'^delete_task$', views.delete_task),
    url(r'^detail$', views.task_detail),
    url(r'^delete_api_test$', views.delete_api_test),
    url(r'^change_select_project', views.change_select_project),
    url(r'^change_select_api', views.change_select_api),
    url(r'^add_api_test', views.add_api_test)
]
