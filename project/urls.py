from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.view),
    url(r'^create_project$', views.add_project),
    url(r'^delete_project$', views.delete_project),
    url(r'^change_project$', views.change_project),
    url(r'^(?P<project_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^[0-9]+/createConfig/$', views.create_config),
    url(r'^(?P<project_id>[0-9]+)/api/',include('api.urls')),
    url(r'^[0-9]+/readConfig/$', views.read_config),
    url(r'^[0-9]+/updateConfig/$', views.update_config),
    url(r'^[0-9]+/deleteConfig/$', views.delete_config),
    url(r'^[0-9]+/createApi/$', views.create_api),
    url(r'^[0-9]+/readApi/$', views.read_api),
    url(r'^[0-9]+/updateApi/$', views.update_api),
    url(r'^[0-9]+/deleteApi/$', views.delete_api),

]
