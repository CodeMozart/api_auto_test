# -*- coding: utf-8 -*-
import requests
from base_validator import *
from api.models import *
from task.models import TimingTask
from api.models import ApiTest
from dashboard.models import ApiTestExecuteLog
import time
import hashlib
import urllib

class TestExecutor:
    def __init__(self, test_id, task_id=0):
        self.test_id = test_id
        self.api_test = ApiTest.objects.get(id=test_id)

        # ---- write by C.M.
        self.api_info = self.api_test.api_info
        self.api_id = self.api_info.id
        self.project_id = self.api_test.project_id
        self.task_id = task_id

        base_url = self.api_info.url
        self.test_method = self.api_test.test_method
        self_param = self.api_test.param
        request_params = CommonRequestParam.objects.filter(api_info=self.api_info)
        param_str = ''

        self.post_dic = dict()
        post_param = self.api_test.post_data
        for post in post_param.split('&'):
            key = post.split('=')[0]
            value = post.split('=')[1]
            self.post_dic[key] = value

        self.api_method = self.api_info.method

        for re_pa in request_params:
            if re_pa.position == 'path':
                param_str += re_pa.key + '=' + re_pa.value + '&'

            elif re_pa.position == 'post':
                self.post_dic[re_pa.key] = re_pa.value
        print str(time.time())
        time_stamp = str(time.time()).split('.')[0]


        # 这里
        aid = self_param.split('&id=')[1].split('&')[0]

        common_param = 'dc40fada41ae5162b1f2b67c2f4cc5fb|ios|200|2.9.7|15|' + time_stamp + '|92205|wP8mtrKnP3jobUr5nwLFn7jPUKO/+STDfsFg1F+htcbhsoW5xvfSGiRhgt1vGQ|2publishApp_Commentlol'+ str(aid) + '00892205a029ae241ef07293bea0286c8d32ddfa211775360582f8097d82d742a044da45'
        _param = 'dc40fada41ae5162b1f2b67c2f4cc5fb|ios|200|2.9.7|15|' + time_stamp + '|92205|wP8mtrKnP3jobUr5nwLFn7jPUKO/+STDfsFg1F+htcbhsoW5xvfSGiRhgt1vGQ|2'
        _param = urllib.quote(_param)
        sig = self.md5(common_param)
        sig = self.md5(sig)

        self.url = base_url + '_param=' + _param + '&' + param_str + self_param + '&sig=' + sig
        print self.url


    def md5(self, str):
        import hashlib
        m = hashlib.md5()
        m.update(str)
        return m.hexdigest()

    def send_request(self):
        if self.api_method == 'get' or self.api_method == 'GET':
            result = self.send_get()
        elif self.api_method == 'post' or self.api_method == 'POST':
            result = self.send_post()
        else:
            result = {
                'status': False,
                'msg': 'Error, invalid api method.'
            }

        api_test = ApiTest.objects.get(id=self.test_id)
        success_run = api_test.success_run
        total_run = api_test.total_run
        fail_run = api_test.fail_run
        total_run += 1

        if result.get('status'):
            # 校验成功
            success_run += 1

        else:
            # 校验失败
            fail_run += 1

        api_test.success_run = success_run
        api_test.total_run = total_run
        api_test.fail_run = fail_run
        api_test.save()

        result['total_run'] = total_run
        result['fail_run'] = fail_run
        result['success_run'] = success_run
        current_time = str(time.time())

        success_data = result.get('success_data')


        execute_log = ApiTestExecuteLog(project_id=int(self.project_id),
                                        test_id=int(self.test_id),
                                        api_id=int(self.api_id),
                                        scheduled=bool(self.task_id),
                                        execute_result=result.get('status'),
                                        error_msg=result.get('msg', 'success'),
                                        success_data=result.get('success_data', 'no data'),
                                        execute_time=current_time,
                                        task_id=self.task_id)

        execute_log.save()

        return result

    def send_get(self):
        try:
            response = requests.get(self.url)
            if 200 <= response.status_code < 400:
                try:
                    response_dict = response.json()
                    return self.validate_response(response_dict)

                except ValueError, e:
                    return {
                        'status': False,
                        'msg': 'Value Error, exception:' + str(e)
                    }
            else:
                return {
                    'status': False,
                    'msg': 'Error, status code :' + response.status_code
                }

        except Exception, e:
            return {
                'status': False,
                'msg': 'Send request fail: ' + str(e)
            }

    def send_post(self):
        try:
            response = requests.post(self.url, data=self.post_dic)
            if 200 <= response.status_code < 400:
                try:
                    response_dict = response.json()
                    return self.validate_post_response(response_dict)
                except ValueError, e:
                    return {
                        'status': False,
                        'msg': 'Value Error, exception:' + str(e)
                    }
            else:
                return {
                    'status': False,
                    'msg': 'Error, status code :' + response.status_code
                }

        except Exception, e:
            return {
                'status': False,
                'msg': 'Send request fail: ' + str(e)
            }

    def validate_post_response(self, response_dict):

        common_validate_not_pass = self.validate_common_data(response_dict)

        if common_validate_not_pass:
            # '''基本校验没有通过'''
            return common_validate_not_pass

        else:
            # """基本校验通过,进入下一步校验"""
            resp_data = response_dict.get('data', {})

            if len(resp_data):
                pass
                return self.validate_response_data(resp_data)
            else:
                # """API 返回数据为空"""
                return {
                    'status': True,
                    'msg': response_dict.get('msg')
                }

    def validate_response(self, response_dict):

        common_validate_not_pass = self.validate_common_data(response_dict)

        if common_validate_not_pass:
            # '''基本校验没有通过'''
            return common_validate_not_pass

        else:
            # """基本校验通过,进入下一步校验"""
            resp_data = response_dict.get('data', {})

            if len(resp_data):
                pass
                return self.validate_response_data(resp_data)
            else:
                # """API 返回数据为空"""
                return {
                    'status': False,
                    'msg': 'Response data is empty!'
                }

    def validate_response_data(self, resp_data):

        # self.api_info
        api_resp = Response.objects.get(api_info=self.api_info)

        resp_bodys = ResponseBody.objects.filter(response=api_resp)

        base_validator = BaseValidator(response_data=resp_data, project_id=self.project_id, api_id=self.api_id, test_id=self.test_id)

        return base_validator.validate(validate_body=resp_bodys, validate_method=self.test_method)

    def validate_common_data(self, response_dict):
        ret = response_dict.get('ret', -1)
        code = response_dict.get('code', -1)
        msg = response_dict.get('msg', 'Unknown error')
        if ret == 0 and code == 0:
            return False
        else:
            print msg
            return {
                'status': False,
                'msg': 'Error, msg: ' + msg
            }


class TimeTaskExecutor:
    def __init__(self, task_id):
        self.task_id = task_id

    def __call__(self, *args, **kwargs):
        timing_task = TimingTask.objects.get(id=self.task_id)
        api_test_list = timing_task.api_test_list
        api_test_id_list = [x for x in api_test_list.split(',')]

        for api_test_id in api_test_id_list:
            test_executor = TestExecutor(test_id=api_test_id, task_id=self.task_id)
            print test_executor.send_request().get('status')
