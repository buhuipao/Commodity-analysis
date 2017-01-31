# _*_ coding: utf-8 _*_

from pymongo import MongoClient
from pymongo import ReturnDocument
from pprint import pprint

from ipdb import set_trace

# 认证连接goods数据库
client = MongoClient('localhost', 27017)
DB = client.goods
DB.authenticate('buhuipao', 'ch19950802qs', mechanism='SCRAM-SHA-1')


def save_result(data):
    try:
        result = DB.Amazon.find_one_and_replace({'name': data['name'], 'key_word': data['key_word']}, data, upsert=True, return_document=ReturnDocument.AFTER)
        pprint(result)
        return result
    except Exception as e:
        print('Save result error:%s' % e)
        return


def find_data(key_word):
    return DB.find({'key_word': key_word})


def update_one(data):
    pass
