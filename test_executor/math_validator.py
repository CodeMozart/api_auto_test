# __author__ = ''
# -*- coding: utf-8 -*-

from math import sqrt
import re


class MathValidator:

    def __init__(self):
        self.cosine = 0
        self.number_list = []
        self.error_message = 'Unknown error!'

    def parse_response(self, response):
        """
        解析出返回数据中的所有数字
        :param response: 
        :return: 所有数字组成的一个list
        """
        if not isinstance(response, list) and (not isinstance(response, dict)):
            return

        if isinstance(response, dict):
            for key in response:
                value = response[key]
                self.number_list = self.__check_value(value, self.number_list)
        elif isinstance(response, list):
            for value in response:
                self.number_list = self.__check_value(value, self.number_list)

        return self.number_list

    def __check_value(self, value, number_list):
        """
        校验每一个value
        :param value: 
        :param number_list: 
        :return: 新的number_list
        """
        if isinstance(value, list) or isinstance(value, dict):
            number_list.extend(self.parse_response(value))
        elif isinstance(value, str) or isinstance(value, unicode):
            pattern = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
            pattern2 = re.compile(r'^[-+]?[0-9]+\.[0-9]+%$')

            if value.isdigit():
                number_list.append(value)
            elif pattern.match(value):
                number_list.append(float(value))
            elif pattern2.match(value):
                number_list.append(float(value[:-1]) / 100)
        else:
            number_list.append(value)
        return number_list

    @staticmethod
    def get_cosine(list_x, list_y):
        """
        计算两个list的夹角余弦
        :param list_x: 
        :param list_y: 
        :return: cos值
        """
        # 取最小个数
        n = min(len(list_x), len(list_y))
        sum_x2 = sum([list_x[i] ** 2 for i in range(n)])
        sum_y2 = sum([list_y[i] ** 2 for i in range(n)])

        sumxy = sum([list_x[i] * list_y[i] for i in range(n)])

        return sumxy / (sqrt(sum_x2) * sqrt(sum_y2))
