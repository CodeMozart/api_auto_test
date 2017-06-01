# coding=utf-8
import os

import logging
import yaml
import json
import copy
from datetime import timedelta

from libs.cache.disk_cache import DiskCache
from libs.crawle.download import Downloader

conf = yaml.load(open(os.path.dirname(__file__) + '/../conf/conf.yaml')).get('wx_work')
if not conf:
    logging.error('Could not get wx_work config.')

api = conf.get('api')
api_access_token = conf.get('api_access_token')
api_contacts = conf.get('api_contacts')
crop_id = conf.get('crop_id')
secret_contacts = conf.get('secret_contacts')
switcher = conf.get('switcher')


def get_access_token_by_secret(secret):
    """
    根据secret获取access token，两小时缓存
    :param secret: 应用的secret
    :return: 应用的access token
    """
    if not secret:
        logging.error('Secret is empty.')
        return

    url = api_access_token % (crop_id, secret)

    try:
        downloader = Downloader(cache=DiskCache(expires=timedelta(seconds=7199)))
        result = json.loads(downloader(url))
        if result.get('errcode') != 0:
            logging.error('Get wx_work access token failed: ' + result.get('errmsg'))
            return ''
        else:
            logging.info('Get wx_work access token : ' + result.get('errmsg'))
            return result.get('access_token')
    except Exception, e:
        logging.error('Get wx_work access token request failed: ' + e.message)
        return ''


def get_user_list_by_department_id(department_id=1, fetch_child=1):
    """
    通过部门ID获取成员列表
    :param department_id: 默认1为玩在一起
    :param fetch_child: 默认1为获取子部门
    :return: 部门成员列表
    """
    access_token = get_access_token_by_secret(secret_contacts)
    url = api_contacts % (department_id, fetch_child, access_token)

    try:
        # access token每两小时变一次，所以以URL为key的缓存最多时效也就是两小时
        downloader = Downloader(cache=DiskCache(expires=timedelta(seconds=7199)))
        result = json.loads(downloader(url))
        if result.get('errcode') != 0:
            logging.error('Get wx_work access token failed: ' + result.get('errmsg'))
            return []
        else:
            logging.info('Get wx_work access token : ' + result.get('errmsg'))
            return result.get('userlist')
    except Exception, e:
        logging.error('Get wx_work access token request failed: ' + e.message)
        return[]


def get_department_id_by_email(emails):
    """
    将邮件和邮件组地址转为部门id
    :param emails: 邮件或者邮件list
    :return: 部门id list
    """

    # 获取所有用户
    user_list = get_user_list_by_department_id()

    if type(emails) is list:
        result_list = list([])
        clone_list = copy.copy(emails)

        # 先替换邮件组地址
        keys = switcher.keys()
        for key in keys:
            if key in clone_list:
                if switcher.get(key) not in result_list:
                    result_list.extend(switcher.get(key))
                clone_list.remove(key)

        # 再替换user邮件地址
        for user in user_list:
            if user.get('userid') in clone_list:
                result_list.extend(user.get('department'))
                clone_list.remove(user.get('userid'))

        # 如果还有邮件地址没有匹配到的话
        if clone_list:
            for email in clone_list:
                logging.warning('Email %s don\'t have a corresponding contact.' % email)

        # 去重
        s = set(result_list)
        result_list = [i for i in s]
        # 去除"玩在一起"部门
        try:
            while True:
                result_list.remove(1)
        except ValueError:
            pass

        return result_list

    elif type(emails) is str:
        result_list = list([])
        # 先替换邮件组地址
        keys = switcher.keys()
        if emails in keys:
            result_list.extend(switcher.get(emails))

        # 再查找用户
        for user in user_list:
            if user.get('userid') == emails:
                result_list = user.get('department')
        # 去重
        s = set(result_list)
        result_list = [i for i in s]
        # 去除"玩在一起"部门
        try:
            while True:
                result_list.remove(1)
        except ValueError:
            pass
        return result_list
    else:
        result_list = list([])
        logging.error('Get phone by email with invalid parameter.')
        return result_list


def get_user_phone_by_email(emails, fetch_department=False):
    """
    通过email获取对应的手机号
    :param emails: email或者email list
    :param fetch_department: 是否需要email对应的部门的所有手机号
    :return: 手机号或者手机号list
    """

    # 获取所有用户
    user_list = get_user_list_by_department_id()

    if type(emails) is list and list:
        result_list = list([])

        # 如果需要某人所在部门的所有手机号
        if fetch_department:
            # 先把email转为部门id
            department_id_list = get_department_id_by_email(emails)

            for department_id in department_id_list:
                for user in user_list:
                    if department_id in user.get('department'):
                        if user.get('mobile') not in result_list:
                            result_list.append(user.get('mobile'))

            return result_list

        else:
            clone_list = copy.copy(emails)
            # 替换user邮件地址
            for user in user_list:
                if user.get('userid') in clone_list:
                    if user.get('mobile') not in result_list:
                        result_list.append(user.get('mobile'))
                    clone_list.remove(user.get('userid'))
            if clone_list:
                for email in clone_list:
                    logging.warning('Email %s don\'t have corresponding a contact.' % email)
            return result_list

    elif type(emails) is str:
        for user in user_list:
            if user.get('userid') == emails:
                return user.get('mobile')
        logging.error('Email %s don\'t have corresponding a contact.' % emails)
        return ''
    else:
        logging.error('Get phone by email with invalid parameter.')
        return ''


def get_department_emails_by_email(email):
    """
    通过email获取同部门下的所有email
    :param email: email 或 email list
    :return: email list
    """
    result_list = list([])

    department_id_list = get_department_id_by_email(email)
    for department_id in department_id_list:
        user_list = get_user_list_by_department_id(department_id=department_id)
        for user in user_list:
            if user.get('email') and user.get('email') not in result_list:
                result_list.append(user.get('email'))

    return result_list
