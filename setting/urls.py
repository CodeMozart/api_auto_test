from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^custom-validator/$', views.custom_validator),
    url(r'^custom-validator/create-custom-validator/$', views.create_custom_validator),
    url(r'^custom-validator/read-custom-validator/$', views.read_custom_validator),
    url(r'^custom-validator/update-custom-validator/$', views.update_custom_validator),
    url(r'^custom-validator/delete-custom-validator/$', views.delete_custom_validator),

]
