# -*- coding: utf-8 -*-
__author__ = "yaoo"
__version__ = "1.0.1"
__email__ = "1711602280@qq.com"

import requests

def getCookies():
    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    }
    sess = requests.Session()
    response = sess.get('https://www.lagou.com/jobs/list_Java?px=default&city=%E5%85%A8%E5%9B%BD#filterBox', headers=headers)

    return response.cookies.get_dict()

if __name__ == '__main__':
    print getCookies()