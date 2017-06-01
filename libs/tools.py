# -*- coding: utf-8 -*-

import urlparse
import datetime
import os
import logging
import yaml
import requests
import csv

from libs.crawle.download import Downloader


def normalize(seed_url, link):
    """
    Normalize this URL by removing hash and adding domain
    """
    link, _ = urlparse.urldefrag(link)  # remove hash to avoid duplicates
    return urlparse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """
    Return True if both URL of belong to same domain
    """
    return urlparse.urlparse(url1).netloc == urlparse.urlparse(url2).netloc


def list2dict(src_list, field):
    """
    list to ditc
    :param src_list: list
    :param field: item
    :return:
    """
    if not list:
        return {}

    data = {}
    for item in src_list:
        # print
        data[item.get(field)] = item

    return data


def str2time(timestamp, format_str='%Y-%m-%d'):
    """
    format timestamp
    :param timestamp:
    :param format_str:
    :return:
    """
    timestamp = int(timestamp)
    date_dict = datetime.datetime.utcfromtimestamp(timestamp)
    return date_dict.strftime(format_str)


def join_sort_list(src_list, join_str='_'):
    """
    :param src_list:
    :param join_str:
    :return:
    """

    src_list.sort()
    return join_str.join(src_list)


def download_img(img_url, save_file):
    download = Downloader(delay=5, num_retries=2)
    img_data = download(img_url)

    # 保持原始图片
    folder = os.path.dirname(save_file)
    if not os.path.exists(folder):
        os.makedirs(folder)

    img_file = open(save_file, "wb")
    img_file.write(img_data)
    img_file.flush()
    img_file.close()


def get_default_value(table_name, node_name=None):
    """
    获取清洗表默认值，在配置文件目录中
    文件名称和表名相同
    """
    def_value = {}
    try:
        def_value = yaml.load(open(os.path.dirname(__file__) + '/../conf/table/' + table_name + '.yaml'))
        if node_name:
            def_value = def_value.get(node_name, {})
    except Exception, e:
        print e

    return def_value


def get_conf(conf_name, node_name=None):
    """
    获取清洗表默认值，在配置文件目录中
    文件名称和表名相同
    """
    def_value = {}
    try:
        def_value = yaml.load(open(os.path.dirname(__file__) + '/../conf/' + conf_name + '.yaml'))
        if node_name:
            def_value = def_value.get(node_name, {})
    except Exception, e:
        print e

    return def_value


def get_conf_by_file_name(file_name, node_name=None):
    """
    获取清洗表默认值，在配置文件目录中
    文件名称和表名相同
    """
    def_value = {}
    try:
        def_value = yaml.load(open(file_name))
        if node_name:
            def_value = def_value.get(node_name, {})
    except Exception, e:
        print e

    return def_value


def int2bin(n, count=11):
    """returns the binary of integer n, using count number of digits"""

    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])


def send_email_by_sendcloud(receiver=list([]), title='', content='', att_file=None):
    """
    发送邮件
    :param receiver: 邮件接收者
    :param title: 邮件标题
    :param content: 邮件内容
    :param att_file: 附件文件名，带路径
    :return:
    """

    conf = get_conf('conf', 'email')
    url = conf.get('url')
    receiver = "%s;%s" % (conf.get('to'), ';'.join(receiver))

    params = {
        "apiUser": conf.get('apiUser'),    # 使用api_user和api_key进行验证
        "apiKey": conf.get('apiKey'),
        "to": receiver,     # 收件人地址, 用正确邮件地址替代, 多个地址用';'分隔
        "from": "noreplay@wanplus.com",     # 发信人, 用正确邮件地址替代
        "fromName": "wanplus_data_support",
        "subject": title,
        "html": content,
    }

    display_filename = "error_list.csv"
    files = dict({})
    if os.path.exists(att_file):
        files['attachments'] = (display_filename, open(att_file, 'rb'), 'application/octet-stream')
    try:
        r = requests.post(url, files=files, data=params)
        logging.info('send_email_by_sendcloud rst: %s' % str(r.text))
    except Exception, e:
        print e


def write_logs_csv(log_name, message):
    """
    写成CSV格式的日志
    :param log_name:
    :param message:
    :return:
    """
    csv_file = file(os.path.dirname(__file__) + '/../data/logs/%s.csv' % log_name, 'a')
    writer = csv.writer(csv_file)
    writer.writerow(message)
    csv_file.close()


def get_avatar(uid, im_size='middle', return_type=0):
    """
    用户头像路径
    :param uid:
    :param im_size:
    :param return_type:
    :return:
    """

    list_size = ['big', 'mid', 'min']
    if im_size not in list_size:
        im_size = 'real'

    uid = int(uid)
    str_uid = "%09d" % uid
    dir1 = str_uid[:3]
    dir2 = str_uid[3:5]
    dir3 = str_uid[5:7]

    if return_type == 1:
        # 目录
        return "%s/%s/%s/" % (dir1, dir2, dir3)

    if return_type == 2:
        # 文件名
        return "%d_%s.jpg" % (uid, im_size)

    # 目录 + 文件名
    return "%s/%s/%s/%d_%s.jpg" % (dir1, dir2, dir3, uid, im_size)