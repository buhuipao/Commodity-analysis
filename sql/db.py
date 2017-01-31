# _*_ coding: utf-8 _*_

from pymongo import MongoClient
from pymongo import ReturnDocument
from pprint import pprint

import time

from ipdb import set_trace

# 认证连接goods数据库
client = MongoClient('localhost', 27017)
DB = client.goods
DB.authenticate('buhuipao', 'ch19950802qs', mechanism='SCRAM-SHA-1')


def save_result(data):
    assert type(data) == dict
    today = time.strftime("%Y-%m-%d", time.time())
    # 增量更新价格
    # 如果存在记录，今天查询过则替换最后搜索的价格否则添加到列表末
    # 不存在则改变数据格式准备之后的存储
    try:
        prices = DB.Amazon.find_one({'name': data['name'], 'key_word': data['key_word']})['price']
        if today not in [price.keys()[0] for price in prices]:
            prices.append({today: data['price']})
            data['price'] = prices
        else:
            prices[-1][today] = data['price']
            data['price'] = prices
    except:
        data['price'] = [{today: data['price']}]

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
