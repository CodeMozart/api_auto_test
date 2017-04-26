# -*- coding: utf-8 -*-
from jsonpath_rw import *
import yaml
import os
from interval import Interval, IntervalSet
import re


class BaseValidator:
    def __init__(self, response_data):
        self.type_conf = yaml.load(open(os.path.dirname(__file__) + '/../conf/field_type.yaml'))
        self.response_data = response_data
        self.error_list = list()

    def validate(self, validate_body):

        for body in validate_body:
            key = body.key
            path = body.path
            type_str = body.type
            type_rule = body.type_rule
            self.validate_field_by_default(path=path, rule=type_rule, type_str=type_str)

        if len(self.error_list):
            # 如果error_list里面有错误信息，说明有字段校验未通过，返回错误信息
            return {
                'status': False,
                'msg': self.error_list
            }

            pass
        else:
            return {
                'status': True,
            }
            pass

    def str_default_validate(self, path, value, rule):

        if re.search(rule, value):
            # 匹配上了正则
            pass
        else:
            error_msg = path + '(value: %s)' % value + ': doesn\'t match the regex: ' + rule
            self.error_list.append(error_msg)

    def int_default_validate(self, path, value, rule):

        if type(value) == str:
            value = eval(value)

        if type(value) != int:
            error_msg = path + '(value: %s)' % value + ': expect a int but a ' + type(value)
            self.error_list.append(error_msg)
        else:
            interval = self.change_rule_to_math_inteval(rule)
            if value in interval:
                pass
            else:
                error_msg = path + '(value: %s)' % value + ': expect in range of ' + rule
                self.error_list.append(error_msg)

    def float_default_validate(self, path, value, rule):

        if type(value) == str:
            value = eval(value)

        if type(value) != int and type(value) != float:
            error_msg = path + '(value: %s)' % value + ': expect a float but a ' + type(value)
            self.error_list.append(error_msg)
        else:
            interval = self.change_rule_to_math_inteval(rule)
            if value in interval:
                pass
            else:
                error_msg = path + '(value: %s)' % value + ': expect in range of ' + rule
                self.error_list.append(error_msg)

    def bool_default_validate(self, path, value, rule):

        if value in (0, 1):
            pass
        else:
            error_msg = path + ': expect a bool(0 or 1) but a value of ' + value
            self.error_list.append(error_msg)

    def dict_default_validate(self, path, value, rule):

        if type(value) == dict:
            pass
        else:
            error_msg = path + ': expect a dict but a ' + type(value)
            self.error_list.append(error_msg)

    def list_default_validate(self, path, value, rule):

        if type(value) == list:
            pass
        else:
            error_msg = path + ': expect a list but a ' + type(value)
            self.error_list.append(error_msg)

    def validate_field_by_default(self, path, rule, type_str):

        method_str = self.type_conf.get('Type').get(type_str)
        jsonpath_expr = parse(path)
        value_list = [match.value for match in jsonpath_expr.find(self.response_data)]

        for value in value_list:
            validate_method = eval('self.' + method_str)
            validate_method(path, value, rule)

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

        if first_char == '(':
            low_closed = False

        if last_char == ')':
            up_closed = False

        intev = Interval(lower_bound=lower_value, upper_bound=upper_value)
        intev.lower_closed = low_closed
        intev.upper_closed = up_closed

        return intev
