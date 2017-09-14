# -*- coding: utf-8 -*-
__author__ = "yaoo"
__version__ = "1.0.1"
__email__ = "1711602280@qq.com"


'''把redis中的json数据转化为MySQL中的数据'''
import redis
import pymysql
from DBUtils.PooledDB import PooledDB
import json
import datetime
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

sh = logging.StreamHandler()
sh.setFormatter(logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s'))
sh.setLevel(logging.DEBUG)

fh = logging.FileHandler('reids-mysql.log', encoding='utf-8')
fh.setFormatter(logging.Formatter('%(asctime)s : %(name)s : %(levelname)s : %(message)s'))
fh.setLevel(logging.INFO)

logger.addHandler(fh)
logger.addHandler(sh)


server = redis.StrictRedis()

pool = PooledDB(pymysql,mincached=10,host='127.0.0.1',user='root',password='123',
         database='crawl',charset='utf8mb4',use_unicode=True)
conn = pool.connection()
cursou = conn.cursor()

def redis_mysql():
    while 1:
            jsonstr = server.brpoplpush('cache','lalgou:position')
            if jsonstr == sentinel:
                break
            try:
                jsonobj = json.loads(jsonstr)
            except Exception as  e:
                server.lrem('lalgou:position', 1, jsonstr)
                continue
            info = jsonobj['content']['positionResult']['result'] # 职位list
            for position_dict in info:
                try:
                    # 插入MySQL
                    companyId=position_dict['companyId'] #(拉钩公司主页的ID)
                    positionName=position_dict['positionName'] #(职位名称)
                    education=position_dict['education'] #(学历)
                    city=position_dict['city']
                    positionId=position_dict['positionId'] #(对应职位详情页)
                    # 转换为对应的url
                    financeStage=position_dict['financeStage'] #(公司融资状态)
                    companyShortName=position_dict['companyShortName'] #(在拉钩显示的公司名称)
                    salary=position_dict['salary']
                    industryField=position_dict['industryField'] #(所属行业)
                    district=position_dict['district'] #工作地点
                    businessZones=position_dict['businessZones'] #(公司商圈)
                    if businessZones:
                        businessZones = ','.join(businessZones)
                    positionAdvantage=position_dict['positionAdvantage'] #(职位诱惑)
                    jobNature=position_dict['jobNature'] #(全职或兼职 实习)
                    workYear=position_dict['workYear']
                    positionLables=position_dict['positionLables'] #(工作职能)
                    positionLables = ','.join(positionLables)
                    companySize=position_dict['companySize']
                    formatCreateTime=position_dict['formatCreateTime'] #(职位发布时间)
                    companyLabelList=position_dict['companyLabelList'] #(公司标签)
                    companyLabelList = ','.join(companyLabelList)
                    companyFullName=position_dict['companyFullName'] #(公司全称)
                    firstType=position_dict['firstType'] #(第一职责)
                    secondType=position_dict['secondType'] #(第二职责)
                    updatetime = datetime.datetime.now()
                    sql='''insert into lagou(companyId,positionName,education,city
                            ,positionId,financeStage,companyShortName,salary,industryField
                            ,district, businessZones,positionAdvantage,jobNature,workYear
                            ,positionLables,companySize,formatCreateTime,companyLabelList
                            ,companyFullName,firstType,secondType,updatetime) VALUES (%s,%s,
                            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            '''
                    params = (companyId,positionName,education,city
                            ,positionId,financeStage,companyShortName,salary,industryField
                            ,district, businessZones,positionAdvantage,jobNature,workYear
                            ,positionLables,companySize,formatCreateTime,companyLabelList
                            ,companyFullName,firstType,secondType,updatetime)
                    cursou.execute(sql,params)
                    conn.commit()
                    logger.debug('ok')
                except Exception as e:
                    if 1062 == e.args[0]:
                        logger.info(e.args[1])
                        continue
                    position_str = json.dumps(position_dict,encoding='utf-8')
                    error_info = str(e)
                    info = error_info+'--------'+position_str.decode('utf-8')
                    logger.error(info)
            server.lrem('lalgou:position', 1, jsonstr)
# def lrem_test():
#     jsonstr = server.brpoplpush('test', 'cache')
#     jsonobj = json.loads(jsonstr)
#     delt = server.lrem('cache', 1 ,jsonstr)
#     print delt
if __name__ == '__main__':
    sentinel = 'is end'
    server.lpush('cache',sentinel)
    redis_mysql()