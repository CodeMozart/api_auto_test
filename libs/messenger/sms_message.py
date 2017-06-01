# coding=utf-8
import os

import logging
import yaml
import requests

from .tool import wx_work_tool
from .notice_flags import *


class SMSMessage:
    """
    短信累
    使用yunpian api发送邮件
    配置文件需要写在同目录下的conf/conf.yaml中
    """
    def __init__(self, recipients=None, subject=None, message=None, attachments=None, option=None):
        """
        构造方法
        :param recipients: 收件人list 不可为空
        :param subject: 邮件主题 不可为空
        :param message: 邮件正文
        :param attachments: 邮件附件路径list
        """
        self.conf = yaml.load(open(os.path.dirname(__file__) + '/conf/conf.yaml')).get('sms')
        if not self.conf:
            logging.error('Could not get SMS config.')
            return

        self.api = self.conf.get('api')
        self.api_key = self.conf.get('api_key')
        if not self.api or not self.api_key:
            logging.error('SMS config error.')
            return

        # 收件人
        self.recipients = [] if recipients is None else recipients
        # 邮件主题
        self.subject = '' if subject is None else subject
        # 邮件正文
        self.message = '' if message is None else message
        # 邮件附件路径
        self.attachments = [] if attachments is None else attachments
        # 配置option
        self.option = 0 if option is None else option

    def send(self):
        """
        发送SMS
        TYPE_FLAG_USER: 发给指定id
        TYPE_FLAG_DEPARTMENT: 发给指定id对应的部门下的所有人
        """
        params = {
            'apikey': self.api_key,  # API_KEY
            'mobile': ','.join(wx_work_tool.get_user_phone_by_email(  # 手机号. 多个地址使用','分隔
                                                emails=self.recipients,
                                                fetch_department=self.option & TYPE_FLAG_DEPARTMENT)),
            'text': self.subject + '\n' + self.message if self.subject else self.message,
        }
        logging.debug('request params:' + str(params))

        try:
            result = requests.post(url=self.api, data=params).json()
            if result.get('code') == 0:
                logging.info('Send SMS message: ' + result.get('msg'))
            else:
                logging.error('Send SMS message failed: ' + result.get('msg'))
        except Exception, e:
            logging.error('Send SMS message request failed: ' + e.message)
            

def send_by_phone(phone, message):
    if not (phone and message):
        logging.error('Send SMS message parameter error.')
        return
    conf = yaml.load(open(os.path.dirname(__file__) + '/conf/conf.yaml')).get('sms')
    if not conf:
        logging.error('Could not get SMS config.')
        return
    api = conf.get('api')
    api_key = conf.get('api_key')
    if not api or not api_key:
        logging.error('SMS config error.')
        return
    params = {
        'apikey': api_key,  # API_KEY
        'mobile': ','.join(phone) if type(phone) is list else phone,
        'text': message,
    }
    try:
        result = requests.post(url=api, data=params).json()
        if result.get('code') == 0:
            logging.info('Send SMS message: ' + result.get('msg'))
        else:
            logging.error('Send SMS message failed: ' + result.get('msg'))
    except Exception, e:
        logging.error('Send SMS message request failed: ' + e.message)
