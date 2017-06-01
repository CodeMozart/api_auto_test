# -*- coding: utf-8 -*-

import json
import time
import urllib
from hashlib import md5
from libs.crawle.download import Downloader

__author__ = 'sk'


class QqLolMatch:
    def __init__(self, cache=None):
        self.cache = cache

    @staticmethod
    def get_list(start, end, page=1):
        url = QqLolMatch.get_list_url(start, end, page)
        return QqLolMatch.request(url)

    @staticmethod
    def get_list_url(start, end, page=1):
        params = dict()
        params['a0'] = 1
        params['p2'] = start
        params['p3'] = end
        params['page'] = page
        return QqLolMatch.format_url(params)

    @staticmethod
    def get_detail(game_id):
        url = QqLolMatch.get_detail_url(game_id)
        return QqLolMatch.request(url)

    @staticmethod
    def get_detail_url(game_id):
        params = dict()
        params['a0'] = 2
        params['p0'] = game_id
        return QqLolMatch.format_url(params)

    @staticmethod
    def format_url(params):
        default = dict()
        default['ua1'] = 7
        default['ua2'] = 2
        default['ua3'] = int(time.time())
        default['ua4'] = QqLolMatch.sign(default['ua1'], default['ua2'], default['ua3'])
        default['p1'] = 107
        default.update(params)

        return 'http://apps.game.qq.com/lol/Go/Entrance/auth?%s' % urllib.urlencode(default)

    @staticmethod
    def request(url):
        d = Downloader()
        response = d(url)
        if not response:
            return False
        return json.loads(response)

    @staticmethod
    def sign(ua1, ua2, ua3):
        m = md5()
        m.update('%s%s%sGcL6DxehO6' % (ua1, ua2, ua3))
        return m.hexdigest()

if __name__ == '__main__':
    api = QqLolMatch()
    s = '2017-04-20'
    e = '2017-04-21'
    try:
        game_list = api.get_list(s, e)
        api.get_detail(game_list.get('msg').get('result').pop().get('BattleId'))
    except Exception as e:
        print str(e)

