# -*- coding: utf-8 -*-
import requests
from base_validator import *
from api.models import *


class TestExecutor:
    def __init__(self, test_id):
        self.test_id = test_id
        self.api_test = ApiTest.objects.get(id=test_id)

        # ---- write by C.M.
        self.api_info = self.api_test.api_info
        base_url = self.api_info.url
        self_param = self.api_test.param
        request_params = CommonRequestParam.objects.filter(api_info=self.api_info)
        param_str = ''

        self.post_dic = dict()
        self.api_method = self.api_info.method

        for re_pa in request_params:
            if re_pa.position == 'path':
                param_str += re_pa.key + '=' + re_pa.value + '&'

            elif re_pa.position == 'post':
                self.post_dic[re_pa.key] = re_pa.value

        self.url = base_url + param_str + self_param

    def send_request(self):
        if self.api_method == 'get' or self.api_method == 'GET':
            return self.send_get()
        elif self.api_method == 'post' or self.api_method == 'POST':
            return self.send_post()
        else:
            return {
                'status': False,
                'msg': 'Error, invalid api method.'
            }

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
                    self.validate_response(response_dict)
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

    def validate_response(self, response_dict):

        common_validate_not_pass = self.validate_common_data(response_dict)

        if common_validate_not_pass:
             # '''基本校验没有通过'''
            return common_validate_not_pass

        else:
            # """基本校验通过,进入下一步校验"""
            resp_data = response_dict.get('data',{})

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

        base_validator = BaseValidator(response_data=resp_data)

        return base_validator.validate(validate_body=resp_bodys)

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
