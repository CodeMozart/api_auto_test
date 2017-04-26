from django.shortcuts import render_to_response, render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from auto_test.views import is_auth
import json
import time


@login_required(login_url="/login/")
def view(request):
    sysinfo = {}
    user = {
        'name': request.user,
        'date': time.time()
    }
    return render(request, 'dashboard/view.html', {'sysinfo': sysinfo, 'user': user})


@is_auth
def get_status_info(request):
    req_status = {}
    r_stat = []
    for r in req_status:
        rs = {
            'req_url': r[0],
            'bytes_in': r[2],
            'bytes_out': r[3],
            'conn_total': r[4],
            'req_total': r[5],
            'http_2xx': r[6],
            'http_3xx': r[7],
            'http_4xx': r[8],
            'http_5xx': r[9]
        }
        r_stat.append(rs)
    context = {
        'flag': "Success",
        'context': {
            "sysstatus": {},
            "reqstatus": r_stat,
            'name': request.user,
        }
    }
    return HttpResponse(json.dumps(context))
