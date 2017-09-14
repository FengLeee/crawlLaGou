# -*- coding: utf-8 -*-
__author__ = "yaoo"
__version__ = "1.0.1"
__email__ = "1711602280@qq.com"

import requests
from scrapy.selector import Selector
import json
def getPosition():
    '''
    获取拉钩职位
    :return:
    '''
    headers = {
        'Host': 'www.lagou.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    }
    response = requests.get('https://www.lagou.com/', headers=headers)
    select = Selector(text=response.text)
    position_list = select.xpath("//div[@class='menu_sub dn']//a/text()").extract()
    with open('position.json','w') as f:
        json.dump(position_list,f,encoding='utf-8')

if __name__ == '__main__':

    getPosition()