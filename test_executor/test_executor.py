# -*- coding: utf-8 -*-
import requests
from base_validator import *
from api.models import *
from project.models import ProjectConfig, Project
from task.models import TimingTask
from api.models import ApiTest
from dashboard.models import ApiTestExecuteLog
import time
import hashlib
import urllib
import hmac
from libs.messenger import MessageSender
from libs.queue.rabbitmq import RabbitAMQP
import base64


class TestExecutor:
    def __init__(self, test_id, task_id=0):
        self.test_id = test_id
        self.appkey_conf = yaml.load(open(os.path.dirname(__file__) + '/../conf/appkey.yaml'))

        try:
            self.api_test = ApiTest.objects.get(id=test_id)
            # ---- write by C.M.
            self.api_info = self.api_test.api_info
            self.api_id = self.api_info.id
            self.project_id = self.api_test.project_id
            self.task_id = task_id

            project = Project.objects.get(id=self.project_id)
            project_config = ProjectConfig.objects.filter(project=project).get(name=self.api_info.url)
            base_url = project_config.base_url
            url_path = self.api_info.url_path
            if base_url[-1] != '/' and url_path[0] != '/':
                base_url += '/'

            self.test_method = self.api_test.test_method
            self_param = self.api_test.param
            request_params = CommonRequestParam.objects.filter(api_info=self.api_info)

            self.post_dic = dict()
            post_param = self.api_test.post_data
            if len(post_param) > 0:
                for post in post_param.split('&'):
                    key = post.split('=')[0]
                    value = post.split('=')[1]
                    self.post_dic[key] = value

            self.api_method = self.api_info.method

            param_dic = self.get_sorted_param_dict(request_params, self_param)

            param_dic_str = self.get_sorted_param_str(param_dic)

            sig_str = str(self.get_sig_param_str(method=self.api_method, url_path=url_path, param_str=param_dic_str))

            try:
                appkey = self.appkey_conf.get('appid').get(int(param_dic.get('appid')))
                secret = appkey + '&'
                secret = secret.replace('-', '+').replace('_', '/')

                sig = urllib.quote_plus(
                    base64.b64encode(
                        hmac.new(key=secret, msg=sig_str, digestmod=hashlib.sha1)
                            .digest()
                    ))

                self.url = base_url + url_path + '?' + param_dic_str + '&sig=' + sig
            except Exception, e:
                self.url = base_url + url_path + '?' + param_dic_str



        except Exception, e:
            task = TimingTask.objects.get(id=task_id)
            api_test_id_list = [x for x in task.api_test_list.split(',')]

            if test_id in api_test_id_list:
                api_test_id_list.remove(test_id)
                str_api_test_list = ','.join(api_test_id_list)
                task.api_test_list = str_api_test_list
                task.save()

    def get_sorted_param_str(self, param_dic):

        a_list = list()
        for param_key in sorted(param_dic.keys()):
            a_list.append(param_key + '=' + param_dic[param_key])

        param_dic_str = '&'.join(a_list)

        return param_dic_str

    def get_sig_param_str(self, method, url_path, param_str):

        strs = method + '&' + urllib.quote_plus(url_path) + '&'

        return strs + urllib.quote_plus(param_str).replace('~', '%7E')

    def get_sorted_param_dict(self, request_params, self_param):

        self_param_list = self_param.split('&')

        param_dic = dict()

        for re_pa in request_params:

            if re_pa.position == 'path':
                param_dic[str(re_pa.key)] = str(re_pa.value)

            elif re_pa.position == 'post':
                self.post_dic[re_pa.key] = re_pa.value

        for index in range(len(self_param_list)):
            str_param = self_param_list[index]
            key = str_param.split('=')[0]
            value = str_param.split('=')[1]
            param_dic[str(key)] = str(value)

        time_stamp = str(time.time()).split('.')[0]
        param_dic['ts'] = time_stamp

        return param_dic

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
        success_data = result.get('success_data', '')
        similarity = result.get('similarity', 0)
        error_msg = result.get('msg', 'success')

        if result.get('status'):
            # 校验成功
            success_run += 1

        else:
            # 校验失败
            fail_run += 1
            project = Project.objects.get(id=self.project_id)
            owner = project.owner
            subject = project.name + ' API ERROR'

            content = unicode(self.api_info.name) + u'\n' + unicode(api_test.name) + u'\n\n' + u'url: ' + unicode(
                self.url) + u'\n' + unicode(error_msg) + u'\nSimilarity: ' + unicode(
                similarity)

            att_file = ''
            mail_receivers = [owner, 'ada@wanplus.com', 'cm@wanplus.com']

            message = dict({})
            message['to'] = mail_receivers
            message['subject'] = subject
            message['content'] = content
            message['att_file'] = att_file
            message['notice_flags'] = 1

            mq = RabbitAMQP()
            mq.publish_message(queue_name='send_message', message_body=message)

            # sender = MessageSender()
            # sender.set_recipients(mail_receivers)
            # sender.set_attachments(att_file)
            # sender.set_option(1)
            # sender.set_subject(subject)
            # sender.set_message(content)
            # sender.send()

        api_test.success_run = success_run
        api_test.total_run = total_run
        api_test.fail_run = fail_run
        api_test.save()

        result['total_run'] = total_run
        result['fail_run'] = fail_run
        result['success_run'] = success_run
        current_time = time.ctime()

        execute_log = ApiTestExecuteLog(project_id=int(self.project_id),
                                        test_id=int(self.test_id),
                                        api_id=int(self.api_id),
                                        scheduled=bool(self.task_id),
                                        execute_result=result.get('status'),
                                        error_msg=error_msg,
                                        success_data=success_data,
                                        execute_time=current_time,
                                        task_id=self.task_id,
                                        similarity=similarity,
                                        url=self.url)

        execute_log.save()

        result['project_id'] = self.project_id

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

        base_validator = BaseValidator(response_data=resp_data, project_id=self.project_id, api_id=self.api_id,
                                       test_id=self.test_id)

        return base_validator.validate(validate_body=resp_bodys, validate_method=self.test_method)

    def validate_common_data(self, response_dict):
        ret = response_dict.get('ret', -1)
        code = response_dict.get('code', -1)
        msg = response_dict.get('msg', 'Unknown error')
        if ret == 0 and code == 0:
            return False
        elif ret == 0 and msg == 'success':
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
