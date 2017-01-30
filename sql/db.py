# _*_ coding: utf-8 _*_

from pymongo import MongoClient
from pprint import pprint

# 认证连接goods数据库
client = MongoClient('localhost', 27017)
db = client.goods
db.authenticate('buhuipao', 'ch19950802qs', mechanism='SCRAM-SHA-1')


def save_result(data):
    try:
        db.Amazon.insert_one(data)
    except Exception as e:
        print('Save result error:%s' % e)
        return


def find_data(data):
    db.find()
