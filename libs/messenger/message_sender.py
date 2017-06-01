# coding=utf-8

from .email_message import *
from .wx_work_message import *
from .sms_message import *
from .notice_flags import *


def new_message():
    return MessageSender()


class MessageSender:
    """
    信息发送类
    调用 EmailMessage WXWorkMessage SMSMessage发送消息
    在 option 中使用 FLAG 进行配置
    TYPE_FLAG_USER：只按照id（email）发送给对应的人
    TYPE_FLAG_DEPARTMENT：发送给id（email）所在的部门的全部成员
    """

    def __init__(self, recipients=None, subject=None, message=None, attachments=None, option=None):
        # 收件人
        self.__recipients = [] if recipients is None else recipients
        # 主题（邮件主题）
        self.__subject = '' if subject is None else subject
        # 消息正文
        self.__message = '' if message is None else message
        # 消息附件
        self.__attachments = [] if attachments is None else attachments
        # 选项flag
        self.__option = 0 if option is None else option

    def set_recipients(self, recipients):
        """设置收件人"""
        if type(recipients) is list:
            self.__recipients = recipients
        else:
            temp_list = list()
            temp_list.append(recipients)
            self.__recipients = temp_list
        return self

    def add_recipient(self, recipient):
        """添加收件人"""
        if type(recipient) is list:
            self.__recipients.extend(recipient)
        else:
            self.__recipients.append(recipient)
        return self

    def set_subject(self, subject):
        """设置主题"""
        self.__subject = subject
        return self

    def set_message(self, message):
        """设置正文"""
        self.__message = message
        return self

    def set_attachments(self, attachments):
        """设置附件"""
        if type(attachments) is list:
            self.__attachments = attachments
        else:
            temp_list = list([])
            temp_list.append(attachments)
            self.__attachments = temp_list
        return self

    def add_attachment(self, attachment):
        """添加附件"""
        if type(attachment) is list:
            self.__attachments.extend(attachment)
        else:
            self.__attachments.append(attachment)
        return self

    def set_option(self, option):
        """设置选项flag"""
        self.__option = option
        return self

    def add_option(self, option):
        """添加选项flag"""
        self.__option = self.__option | option
        return self

    def send(self):
        # 收信人为空
        if not self.__recipients:
            logging.error('Recipients is EMPTY.')
            return
        # 发邮件主题为空
        if ((not self.__option & PLATFORM_MASK) or self.__option & PLATFORM_FLAG_EMAIL) \
                and not self.__subject:
            logging.error('Subject is EMPTY while sending email.')
            return
        # 主题 内容全为空
        if (not self.__subject) and (not self.__message):
            logging.error('One if subject, message is EMPTY.')
            return

        if (not self.__option & PLATFORM_MASK) or self.__option & PLATFORM_FLAG_EMAIL:
            EmailMessage(recipients=self.__recipients, subject=self.__subject,
                         message=self.__message, attachments=self.__attachments,
                         option=self.__option).send()

        if (not self.__option & PLATFORM_MASK) or self.__option & PLATFORM_FLAG_SMS:
            SMSMessage(recipients=self.__recipients, subject=self.__subject,
                       message=self.__message, attachments=self.__attachments,
                       option=self.__option).send()

        # 在使用部门方式发送时，会将self.__recipients中的邮件替换成部门id
        if (not self.__option & PLATFORM_MASK) or \
                self.__option & PLATFORM_FLAG_WX_WORK_GAREN or \
                self.__option & PLATFORM_FLAG_WX_WORK_DATA_ASSISTANT:
            WXWorkMessage(recipients=self.__recipients, subject=self.__subject,
                          message=self.__message, attachments=self.__attachments,
                          option=self.__option).send()
