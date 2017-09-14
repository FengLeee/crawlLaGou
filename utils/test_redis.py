# -*- coding: utf-8 -*-
__author__ = "yaoo"
__version__ = "1.0.1"
__email__ = "1711602280@qq.com"

import redis

db = redis.Redis(host='13.114.150.42', port=6379, db=0, password=123)
db.set('name', 'xiaoliu')
print (db.get('name'))