# coding=utf-8
import os

import logging
import yaml
import requests

from .notice_flags import *
from .tool import wx_work_tool


class EmailMessage:
    """
    邮件类
    使用sendcloud api发送邮件
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
        self.conf = yaml.load(open(os.path.dirname(__file__) + '/conf/conf.yaml')).get('email')
        if not self.conf:
            logging.error('Could not get email config.')
            return

        self.api = self.conf.get('api')
        self.api_user = self.conf.get('api_user')
        self.api_key = self.conf.get('api_key')
        if not self.api or not self.api_user or not self.api_key:
            logging.error('Email config error.')
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
        """发送邮件"""
        params = {
            'apiUser': self.api_user,  # API_USER
            'apiKey': self.api_key,  # API_KEY
            'from': "messenger<noreply@www.wanplus.com>",  # 发件人地址
            'to': ';'.join(wx_work_tool.get_department_emails_by_email(self.recipients)
                           if self.option & TYPE_FLAG_DEPARTMENT else self.recipients),  # 收件人地址. 多个地址使用';'分隔
            'subject': self.subject,  # 标题. 不能为空
            'fromName': "messenger<noreply@www.wanplus.com>",
            'plain': self.message,  # 邮件的内容. 邮件格式为 text/plain
        }
        logging.debug('request params:' + str(params))

        files = list([])
        for attachment in self.attachments:
            if os.path.exists(attachment):
                files.append(('attachments', open(attachment, 'rb')))

        try:
            response = requests.post(url=self.api, data=params, files=files).json()
            if response.get('result'):
                logging.info('Send email message: ' + response.get('message'))
            else:
                logging.error('Send email message failed: ' + response.get('message'))
        except Exception, e:
            logging.error('Send email message request failed: ' + e.message)
