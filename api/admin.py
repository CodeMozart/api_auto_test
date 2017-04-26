from django.contrib import admin
from models import *
# Register your models here.

admin.site.register(ApiInfo)
admin.site.register(CommonRequestParam)
admin.site.register(Response)
admin.site.register(ResponseHeader)
admin.site.register(KeyType)
# admin.site.register(TypeRule)
admin.site.register(ResponseBody)
admin.site.register(ApiTest)
admin.site.register(ApiTestMethod)
admin.site.register(ApiTestTaskType)