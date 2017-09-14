# -*- coding: utf-8 -*-
__author__ = "yaoo"
__version__ = "1.0.1"
__email__ = "1711602280@qq.com"


'''使用线程池爬取拉钩'''
import logging
import threading
import requests
import json
import Queue
import random
import redis
import time
from utils.lagou_cookie import getCookies

# 职位名称
with open('position.json','r') as f:
    position_list = json.load(f)
# 入队列
position_queue = Queue.Queue()
for position in position_list:
    position_queue.put(position)

# 获取cookies
cookies = getCookies()
# 拼凑cookies
cookies['LGUID'] = cookies['user_trace_token']

# 获取UA
with open('ua_list.json', 'r') as f:
    ualist = json.load(f)
url = 'https://www.lagou.com/jobs/positionAjax.json?px=default&needAddtionalResult=false&isSchoolJob=0'
headers = {
    'Referer': 'https://www.lagou.com/jobs/list_java?&city=%E5%85%A8%E5%9B%BD',
    # 'X-Forwarded-For': '{}.{}.{}.{},113.110.231.123'.format(random.randint(1,254),random.randint(1,254),random.randint(1,254),random.randint(1,254))
}
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s')

fh = logging.FileHandler('lg.log',encoding='utf-8')
fh.setLevel(logging.INFO)
fh.setFormatter(formatter)

sh = logging.StreamHandler()
sh.setLevel(logging.DEBUG)
sh.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(sh)

server = redis.StrictRedis()


class Taskcrawl(threading.Thread):
    def __init__(self,headers,name):
        # 线程初始化
        super(Taskcrawl,self).__init__()
        self.headers=headers
        self.name=name

    def run(self):
        while 1:
            try:
                position = position_queue.get()
                if position is sentinel:
                    position_queue.put(position)
                    break
                index = 1
                j = 0
                while 1:
                    # 需要构造参数传递
                    form_data = {
                        'first': 'false',
                        'pn': index,
                        'kd': position
                    }
                    self.headers['User-Agent'] = random.choice(ualist)
                    try:
                        print 'threading-%s is running: position is: %s index is  %s' % (self.name, position, index)
                        response = requests.post(url=url, data=form_data, headers=self.headers, cookies=cookies)
                        jsonobj = json.loads(response.text, encoding='utf-8')
                        # 放入redis
                        if jsonobj['content']['pageNo'] == 0:
                            print 'threading-%s is running: position is: %s index is  %s crawl over' % (self.name, position, index)
                            break
                        server.lpush('lagou:position', response.text)
                    except Exception as e:
                        if j<2 and response.url!=200:
                            time.sleep(2)
                            j+=1
                            continue
                        else:
                            info = str(e).decode('utf-8')
                            message = info + position + str(index)
                            logger.error(message)
                            fh.flush()
                    j=0
                    index += 1
                position_queue.task_done()
            except Exception as e:
                info = str(e).decode('utf-8')
                message = info
                logger.error(message)
                fh.flush()


class Pool(object):
    '''
    自定义线程池
    '''
    def __init__(self,size):
        self.size = size
        self.threads = [Taskcrawl(headers,name=i) for i in range(self.size)]

    def start(self):
        for task in self.threads:
            task.start()

    def check_alive(self):
        for task in self.threads:
            if task.is_alive():
                print task.name+'is alive'
            else:
                print task.name + 'is dead'

    def stop(self, sentinel):
        position_queue.put(sentinel)

    def join(self):
        for task in self.threads:
            task.join()

if __name__ == '__main__':
    sentinel = object()
    p = Pool(16)
    p.start()
    position_queue.join()
    p.stop(sentinel)
    p.join()
    p.check_alive()
    print 'processor is ending =============='