from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.view),
    url(r'^(?P<api_id>[0-9]+)/execute_api_test/$', views.execute_api_test),
    url(r'^(?P<api_id>[0-9]+)/add_request_param/$', views.add_request_param),
    url(r'^(?P<api_id>[0-9]+)/change_request_param/$', views.change_request_param),
    url(r'^(?P<api_id>[0-9]+)/add_resp_header/$', views.add_resp_header),
    url(r'^(?P<api_id>[0-9]+)/change_resp_header/$', views.change_resp_header),
    url(r'^(?P<api_id>[0-9]+)/delete_resp_header/$', views.delete_resp_header),
    url(r'^(?P<api_id>[0-9]+)/select_resp_body_type/$', views.select_resp_body_type),
    url(r'^(?P<api_id>[0-9]+)/add_resp_body/$', views.add_resp_body),
    url(r'^(?P<api_id>[0-9]+)/change_resp_body/$', views.change_resp_body),
    url(r'^(?P<api_id>[0-9]+)/delete_resp_body/$', views.delete_resp_body),
    url(r'^(?P<api_id>[0-9]+)/add_api_test/$', views.add_api_test),
    url(r'^(?P<api_id>[0-9]+)/change_api_test/$', views.change_api_test),
    url(r'^(?P<api_id>[0-9]+)/delete_api_test/$', views.delete_api_test),
    url(r'^(?P<api_id>[0-9]+)/change_api_base_info/$', views.change_api_base_info),
    url(r'^(?P<api_id>[0-9]+)/delete_request_param/$', views.delete_request_param),
    url(r'^(?P<api_id>[0-9]+)/$', views.detail_view, name='detail_view'),

    # url(r'^[0-9]+/deleteConfig/$', views.delete_config)
]
