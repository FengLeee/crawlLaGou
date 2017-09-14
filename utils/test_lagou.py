# -*- coding: utf-8 -*-
__author__ = "yaoo"
__version__ = "1.0.1"
__email__ = "1711602280@qq.com"

import time
import requests
import json

# url = 'https://httpbin.org/get?show_env=1'
url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'


cookies = {
    'JSESSIONID': 'ABAAABAAAIAACBI7E9D6AB63F8C9D531152A1EAF8EE198B' ,
    ' user_trace_token': '20170826105745-55e63a82-8a0a-11e7-8edc-5254005c3644' ,
    ' LGUID': '20170826105745-55e63e24-8a0a-11e7-8edc-5254005c3644' ,
    ' SEARCH_ID': 'c70b36db1d324e00bd067743c41fd468' ,
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Referer': 'https://www.lagou.com/jobs/list_java?&city=%E5%85%A8%E5%9B%BD',
    'X-Forwarded-For': '113.87.161.12'
}

index = 1
while 1:
    form_data = {
        'first': 'false',
        'pn': index,
        'kd': 'java'
    }
    response = requests.post(url=url, data=form_data, headers=headers, cookies=cookies)
    print response.text
    jsonobj = json.loads(response.text,encoding='utf-8')
    if jsonobj['content']['pageNo'] == 0:
        break
    index+=1