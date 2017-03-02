# _*_ coding: utf-8 _*_

from pymongo import ReturnDocument
from pprint import pprint
from pymongo import MongoClient
from bson import json_util

import time

from ipdb import set_trace

# 认证连接goods数据库
client = MongoClient('localhost', 27017)
DB = client.goods
DB.authenticate('buhuipao', 'ch19950802qs', mechanism='SCRAM-SHA-1')


def save_search_result(data):
    '''
     增量更新价格, 如果不存在记录则新建， 存在则判断今天的价格是否存在,
     如果今日的价格存在则先弹出再增加，否则直接增加, 返回更新后的文档
    '''
    assert type(data) == dict
    assert type(data['price']) == float
    today = int(time.strftime("%Y%m%d"))
    name = data['name']
    key_word = data['key_word']
    prices = {'date': today, 'price': data['price']}
    data.pop('price')
    try:
        old_data = DB.Amazon.find_one({'name': name, 'key_word': key_word})
        if not old_data:
            data['prices'] = [prices]
            DB.Amazon.insert_one(data)
            return data
        else:
            # 如果今日的纪录存在，先弹出压入保存
            if 'prices' in old_data.keys() and today in old_data['prices'][-1].values():
                # {'$pop': {'prices': 1}}表示从prices列表里正序弹栈
                DB.Amazon.find_one_and_update(
                        {'name': name, 'key_word': key_word},
                        {'$pop': {'prices': 1}})
            return DB.Amazon.find_one_and_update(
                    {'name': name, 'key_word': key_word},
                    {'$push': {'prices': prices},
                     '$set': {'same': data['same']}},
                    {'_id': 0},
                    return_document=ReturnDocument.AFTER)
    except Exception as e:
        raise Exception('%s' % e)


def search_goods(limit_price, key_word):
    '''
    传入两个参数，分别为：最低价格，关键字
    '''
    result = json_util.dumps(DB.Amazon.find(
        {'key_word': key_word,
         'prices.price': {'$gte': limit_price}},
        {'_id': 0}))
    return json_util.loads(result)


def find_one_goods(key_word, goods_name):
    return DB.Amazon.find_one(
            {'key_word': key_word, 'name': goods_name},
            {'_id': 0})


def update_proxy(proxy, state):
    # 先清理再更新代理IP数据库
    DB.ProxyIP.remove({'state': False})
    ip, port = proxy['ip'], proxy['port']
    DB.ProxyIP.find_one_and_replace(
            {'ip': ip, 'port': port},
            {'ip': ip, 'port': port, 'state': state},
            upsert=True)


def find_porxy():
    # 先清理不可用的代理('state'==False), 接着返回所有可用的代理
    DB.ProxyIP.remove({'state': False})
    result = json_util.dumps(DB.ProxyIP.find({'state': True}, {'_id': 0}))
    return json_util.loads(result)
