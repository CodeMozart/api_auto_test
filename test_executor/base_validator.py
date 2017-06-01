# -*- coding: utf-8 -*-
from jsonpath_rw import *
import yaml
import os
from interval import Interval, IntervalSet
from setting.models import CustomValidateRule
from dashboard.models import ApiTestExecuteLog
from custom_validator import CustomValidator
import re
from math_validator import *
import json


class BaseValidator:
    def __init__(self, response_data, api_id, project_id, test_id):
        self.type_conf = yaml.load(open(os.path.dirname(__file__) + '/../conf/field_type.yaml'))
        self.response_data = response_data
        self.error_list = list()
        self.api_id = api_id
        self.test_id = test_id
        self.project_id = project_id
        self.history_data_list = ApiTestExecuteLog.objects.filter(api_id=api_id)

    def validate(self, validate_body, validate_method):

        # 这里是api的基本检查
        for body in validate_body:
            key = body.key
            path = body.path
            type_str = body.type
            type_rule = body.type_rule
            self.validate_field_by_default(path=path, rule=type_rule, type_str=type_str)

        # 这里是api自定义检查
        custom_rule = CustomValidateRule.objects.get(name=validate_method)

        if not custom_rule.is_default:
            custom_validator = CustomValidator(rule_id=custom_rule.id)
            if custom_validator(self.response_data):
                self.error_list.append(custom_validator(self.response_data))

        # # 这里是数学检查
        # cos_result = 0
        #
        # list_x = parse_response(self.response_data)
        #
        # api_log_list = ApiTestExecuteLog.objects.filter(api_id=self.api_id, project_id=self.project_id,
        #                                                 test_id=self.test_id, execute_result=True)
        # if len(api_log_list) > 0:
        #     last_resp_data = api_log_list[len(api_log_list) - 1].success_data
        #     last_resp_data = json.loads(last_resp_data)
        #     list_y = parse_response(last_resp_data)
        #     cos_result = get_cosine(list_x, list_y)

        # 返回验证结果
        if len(self.error_list):
            # 如果error_list里面有错误信息，说明有字段校验未通过，返回错误信息
            return {
                'status': False,
                'msg': self.error_list,
            }
        else:
            return {
                'status': True,
                'success_data': json.dumps(self.response_data),
            }

    def str_default_validate(self, path, value, rule):

        if type(value) == str or type(value) == unicode:
            if re.search(rule, value):
                # 匹配上了正则
                pass
            else:
                error_msg = str(path) + '(value: %s)' % value + ': doesn\'t match the regex: ' + str(rule)
                self.error_list.append(error_msg)
        else:
            error_msg = str(path) + str(': expect a str but a ') + str(type(value))
            self.error_list.append(error_msg)

    def int_default_validate(self, path, value, rule):

        if type(value) == str or type(value) == unicode:
            value = str(value)
            try:
                value = eval(value)
            except Exception,e:
                pass

        if type(value) != int:
            error_msg = str(path) + '(value: %s)' % value + ': expect a int but a ' + str(type(value))
            self.error_list.append(error_msg)
        else:
            interval = self.change_rule_to_math_inteval(rule)
            if value in interval:
                pass
            else:
                error_msg = str(path) + '(value: %s)' % value + ': expect in range of ' + str(rule)
                self.error_list.append(error_msg)

    def float_default_validate(self, path, value, rule):

        if type(value) == str or type(value) == unicode:
            value = str(value)
            try:
                value = eval(value)
            except Exception,e:
                # 尝试用匹配百分比的正则来处理
                pa = '^(100|[1-9]?\d(\.\d\d?)?)%$'
                if re.match(pa,str(value)):
                    print value
                    value = value.rstrip('%')
                    try:
                        value = eval(value)
                        value = value / 100.0
                    except Exception,e:
                        pass
                else:
                    print value

        if type(value) != int and type(value) != float:
            error_msg = str(path) + '(value: %s)' % value + ': expect a float but a ' + str(type(value))
            self.error_list.append(error_msg)
        else:
            interval = self.change_rule_to_math_inteval(rule)
            if value in interval:
                pass
            else:
                error_msg = str(path) + '(value: %s)' % value + ': expect in range of ' + str(rule)
                self.error_list.append(error_msg)

    def bool_default_validate(self, path, value, rule):

        if value in (0, 1):
            pass
        else:
            error_msg = str(path) + ': expect a bool(0 or 1) but a value of ' + str(value)
            self.error_list.append(error_msg)

    def dict_default_validate(self, path, value, rule):

        if type(value) == dict:
            pass
        else:
            error_msg = str(path) + ': expect a dict but a ' + str(type(value))
            self.error_list.append(error_msg)

    def list_default_validate(self, path, value, rule):

        if type(value) == list:
            pass
        else:
            error_msg = str(path) + ': expect a list but a ' + str(type(value))
            self.error_list.append(error_msg)

    def validate_field_by_default(self, path, rule, type_str):

        method_str = self.type_conf.get('Type').get(type_str)
        jsonpath_expr = parse(path)
        value_list = [match.value for match in jsonpath_expr.find(self.response_data)]

        # 获取此字段历史数据
        history_value_list = self.get_history_value_list(jsonpath_expr)

        for value in value_list:
            validate_method = eval('self.' + method_str)
            validate_method(path, value, rule)

            # 是否需要数值校验
            if self.check_number(value):
                math_validator = MathValidator(current_value=value, history_value_list=history_value_list)
                result = math_validator.check_start()
                if result < 0.05 or result > 0.95:
                    self.error_list.append('数学校验出现异常，请检查数据，path=%s, reslut=%s' % (path, result))

    def get_history_value_list(self, jsonpath_expr):
        history_value_list = []
        for history_data in self.history_data_list:
            history_response = history_data.success_data
            history_response_value_list = [match.value for match in jsonpath_expr.find(history_response)]
            if len(history_response_value_list) == 1:
                history_value_list.append(history_response_value_list[0])
        return history_value_list

    @staticmethod
    def change_rule_to_math_inteval(rule):
        rule = rule.replace(' ', '')
        first_char = rule[0:1]
        last_char = rule[-1:]
        mid_str = rule[1:-1]

        try:
            upper_value = float(mid_str.split(',')[1])
        except:
            upper_value = float('inf')

        try:
            lower_value = float(mid_str.split(',')[0])
        except:
            lower_value = float('-inf')

        low_closed = True
        up_closed = True

        if first_char == '(' or first_char == '（':
            low_closed = False

        if last_char == ')' or last_char == '）':
            up_closed = False

        intev = Interval(lower_bound=lower_value, upper_bound=upper_value)
        intev.lower_closed = low_closed
        intev.upper_closed = up_closed

        return intev

    @staticmethod
    def check_number(value):
        res = False
        if isinstance(value, list) or isinstance(value, dict):
            res = False
        elif isinstance(value, str) or isinstance(value, unicode):
            pattern = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
            pattern2 = re.compile(r'^[-+]?[0-9]+\.[0-9]+%$')

            if value.isdigit():
                res = True
            elif pattern.match(value):
                res = True
            elif pattern2.match(value):
                res = True
        else:
            res = True
        return res
