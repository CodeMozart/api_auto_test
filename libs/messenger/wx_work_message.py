# coding=utf-8
import json
import os

import logging
import requests
import yaml

from .notice_flags import *
from .tool import wx_work_tool


class WXWorkMessage:
    """
    企业微信类
    使用企业微信api给指定成员发送消息
    配置文件需要写在同目录下的conf/conf.yaml中
    """

    def __init__(self, recipients=None, subject=None, message=None, attachments=None, option=None):
        """
        构造方法
        :param recipients: 收信人Wanplus邮箱list 不可为空
        :param subject: 主题 由于这不是邮件，可以为空
        :param message: 消息 不可为空
        :param attachments: 附件文件路径list
        """
        self.conf = yaml.load(open(os.path.dirname(__file__) + '/conf/conf.yaml')).get('wx_work')
        if not self.conf:
            logging.error('Could not get wx_work config.')
            return

        self.api = self.conf.get('api')
        self.api_access_token = self.conf.get('api_access_token')
        self.api_upload = self.conf.get('api_upload')
        self.crop_id = self.conf.get('crop_id')
        self.secret_garen = self.conf.get('secret_garen')
        self.secret_data_assistant = self.conf.get('secret_data_assistant')
        self.secret_contacts = self.conf.get('secret_contacts')

        if not self.crop_id or not self.secret_garen or not self.secret_data_assistant or not self.secret_contacts:
            logging.error('wx_work config error.')
            return

        # 收信人
        self.recipients = [] if recipients is None else recipients
        # 主题
        self.subject = '' if subject is None else subject
        # 消息
        self.message = '' if message is None else message
        # 附件文件路径
        self.attachments = [] if attachments is None else attachments
        # 配置option
        self.option = 0 if option is None else option
        # 与 agentid 对应的 access token
        self.access_token = ''
        # 与 access token 对应的 agentid
        self.agent_id = 0
        # 已经上传了的附件的 media id
        self.media_ids = []

        self.get_access_token()

    def get_access_token(self):
        """获取配置对应的应用的 access token"""
        # 默认使用玩加盖伦
        if (not self.option & PLATFORM_MASK) or \
                self.option & PLATFORM_FLAG_WX_WORK_GAREN:
            self.access_token = wx_work_tool.get_access_token_by_secret(self.secret_garen)

            self.agent_id = int(self.conf.get('agent_id_garen'))
        elif self.option & PLATFORM_FLAG_WX_WORK_DATA_ASSISTANT:
            self.access_token = wx_work_tool.get_access_token_by_secret(self.secret_data_assistant)
            self.agent_id = int(self.conf.get('agent_id_data_assistant'))

    def upload_file(self):
        """上传附件"""
        self.api_upload %= self.access_token

        # 不能一次上传多个，只能分次上传
        for attachment in self.attachments:
            if os.path.exists(attachment):
                files = {
                    'media': open(attachment, 'rb')
                }
                try:
                    result = requests.post(self.api_upload, files=files).json()
                    if result.get('errcode') == 0:
                        logging.info('Upload file to wx_work: ' + result.get('errmsg'))
                        self.media_ids.append(result.get('media_id'))
                    else:
                        logging.error('Upload file to wx_work failed: ' + result.get('errmsg'))
                except Exception, e:
                    logging.error('Upload file to wx_work request failed: ' + e.message)

    def send(self):
        """
        发送企业微信消息
        TYPE_FLAG_USER: 发给指定id
        TYPE_FLAG_DEPARTMENT: 发给指定id对应的部门下的所有人
        """
        url = self.api % self.access_token

        # 先上传附件
        self.upload_file()

        # 最后发送文本消息
        if self.option & TYPE_FLAG_DEPARTMENT:
            # 根据email获取部门id
            recipients = wx_work_tool.get_department_id_by_email(self.recipients)

            # 分次发送附件消息
            for media_id in self.media_ids:
                params = {
                    'toparty': '|'.join(map(str, recipients)),
                    'msgtype': 'file',
                    'agentid': self.agent_id,
                    'file': {
                        'media_id': media_id
                    }
                }
                try:
                    result = requests.post(url=url, data=json.dumps(params)).json()
                    if result.get('errcode') == 0:
                        logging.info('Send file message to wx_work: ' + result.get('errmsg'))
                    else:
                        logging.error('Send file message to wx_work failed: ' + result.get('errmsg'))
                except Exception, e:
                    logging.error('Send file message to wx_work request failed: ' + e.message)

            params = {
                'toparty': '|'.join(map(str, recipients)),
                'msgtype': 'text',
                'agentid': self.agent_id,
                'text': {
                    'content': self.subject + '\n' + self.message if self.subject else self.message
                }
            }
        else:
            # 分次发送附件消息
            for media_id in self.media_ids:
                params = {
                    'touser': '|'.join(self.recipients),
                    'msgtype': 'file',
                    'agentid': self.agent_id,
                    'file': {
                        'media_id': media_id
                    }
                }
                try:
                    result = requests.post(url=url, data=json.dumps(params)).json()
                    if result.get('errcode') == 0:
                        logging.info('Send file message to wx_work: ' + result.get('errmsg'))
                    else:
                        logging.error('Send file message to wx_work failed: ' + result.get('errmsg'))
                except Exception, e:
                    logging.error('Send file message to wx_work request failed: ' + e.message)

            self.recipients = map(str, self.recipients)
            params = {
                'touser': '|'.join(self.recipients),
                'msgtype': 'text',
                'agentid': self.agent_id,
                'text': {
                    'content': self.subject + '\n' + self.message if self.subject else self.message
                }
            }
        try:
            logging.debug('request params:' + str(params))
            result = requests.post(url=url, data=json.dumps(params)).json()
            if result.get('errcode') == 0:
                logging.info('Send text message to wx_work: ' + result.get('errmsg'))
            else:
                logging.error('Send text message to wx_work failed: ' + result.get('errmsg'))
        except Exception, e:
            logging.error('Send text message to wx_work request failed: ' + e.message)
