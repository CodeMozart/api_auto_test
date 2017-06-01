# __author__ = ''
# -*- coding: utf-8 -*-

from math import sqrt
import re
import random
import numpy


class MathValidator:
    def __init__(self, current_value, history_value_list):

        self.current_value = self.transform_number(current_value)
        self.history_value_list = [self.transform_number(value) for value in history_value_list]
        self.new_value_list = []
        self.error_message = 'Unknown error!'
        self.mean = 0
        self.variance = 0
        self.min_value = 0
        self.max_value = 0

    def translate_history_data(self):
        self.mean = numpy.average(self.history_value_list)
        self.variance = numpy.var(self.history_value_list)
        self.min_value = numpy.min(self.history_value_list)
        self.max_value = numpy.max(self.history_value_list)
        # 归一化
        return [self.normalization(value) for value in self.history_value_list]

    def check_start(self):
        # 如果历史数据量少于100，则不进行校验
        if len(self.new_value_list) < 100:
            return 0.5
        else:
            self.new_value_list = self.translate_history_data()
            # 对本次的value进行归一化
            result = self.normalization(self.current_value)
            return self.st_normal(result)

    def normalization(self, x):
        """
        归一化方法
        :param x: 
        :return: 
        """
        x1 = (x - self.mean) / sqrt(self.variance)
        # x1 = float(x - self.min_value) / float(self.max_value - self.min_value)
        return x1

    def st_normal(self, u):
        """
        计算在标准正态分布中的概率
        :param u: 
        :return: 概率p  0～1之间
        """
        import math
        x = abs(u) / math.sqrt(2)
        T = (0.0705230784, 0.0422820123, 0.0092705272,
             0.0001520143, 0.0002765672, 0.0000430638)
        E = 1 - pow((1 + sum([a * pow(x, (i + 1))
                              for i, a in enumerate(T)])), -16)
        p = 0.5 - 0.5 * E if u < 0 else 0.5 + 0.5 * E
        return p

    @staticmethod
    def transform_number(original_number):
        """
        转换成数字
        :param original_number: 可能是数字或字符串
        :return: 数字
        """
        new_number = 0
        if isinstance(original_number, list) or isinstance(original_number, dict):
            new_number = 0
        elif isinstance(original_number, str) or isinstance(original_number, unicode):
            pattern = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
            pattern2 = re.compile(r'^[-+]?[0-9]+\.[0-9]+%$')

            if original_number.isdigit():
                new_number = float(original_number)
            elif pattern.match(original_number):
                new_number = float(original_number)
            elif pattern2.match(original_number):
                new_number = (float(original_number[:-1]) / 100)
        else:
            new_number = original_number
        return new_number


# ---------------------------------  分割线 相似性计算  -----------------------------
def parse_response(response):
    """
    解析出返回数据中的所有数字
    :param response: 
    :return: 所有数字组成的一个list
    """
    if not isinstance(response, list) and (not isinstance(response, dict)):
        return

    number_list = []
    if isinstance(response, dict):
        for key in response:
            value = response[key]
            number_list = check_value(value, number_list)
    elif isinstance(response, list):
        for value in response:
            number_list = check_value(value, number_list)

    return number_list


def check_value(value, number_list):
    """
    校验每一个value
    :param value: 
    :param number_list: 
    :return: 新的number_list
    """
    if isinstance(value, list) or isinstance(value, dict):
        number_list.extend(parse_response(value))
    elif isinstance(value, str) or isinstance(value, unicode):
        pattern = re.compile(r'^[-+]?[0-9]+\.[0-9]+$')
        pattern2 = re.compile(r'^[-+]?[0-9]+\.[0-9]+%$')

        if value.isdigit():
            number_list.append(float(value))
        elif pattern.match(value):
            number_list.append(float(value))
        elif pattern2.match(value):
            number_list.append(float(value[:-1]) / 100)
    else:
        number_list.append(value)
    return number_list


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


if __name__ == '__main__':

    number_list = []

    math1 = MathValidator(10, number_list)
    varrr = math1.translate_history_data()
    print numpy.var(varrr)
    xx = math1.normalization(600)
    print math1.st_normal(xx)

    # print math1.get_cosine(list1, list2)



