# _*_ coding: utf-8 _*_

import requests
import random
from lxml import etree

from configs import USER_AGENTS
from sql import db


class Amazon(object):
    def __init__(self):
        self.url = 'https://www.amazon.cn/s/ref=sr_pg_1'

    def get_result(self, key_word, page_number):
        print('Start search goods...')
        headers = {'User-Agent': random.choice(USER_AGENTS), # 随机组装浏览器访问头，抵抗反爬虫技术
             'Host': 'www.amazon.cn',
             'Accept': 'text/html,application/xhtml+xml,application/xml;\
                        q=0.9,image/webp,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate, sdch, br',
             'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
             }
        payload = {'ie': 'UTF8', 'keywords': key_word, 'page': page_number}

        '''
        while True:
            # 假设代理数据库里有可用代理IP（即proxy不为空），否则就采用本机IP为代理
            proxy = random.choice(db.find_porxy()) \
                    if len(db.find_porxy()) != 0 else None
            if proxy:
                # 假如代理IP不为空，就组装代理IP，然后用代理IP访问Amazon得到商品信息
                data = {'http': 'http://'+proxy['ip']+':'+proxy['port'],
                        'https': 'http://'+proxy['ip']+':'+proxy['port']}
            else:
                # 没有代理IP，那么就设为空，即使用本地IP访问Amazon得到商品信息
                data = {}
            try:
                r = requests.get(self.url, params=payload, headers=headers, proxies=data)
                if r.status_code == 200:
                    break
            except:
                # 如果用的本机IP访问Amazon出错就提示检查网络, 否则就更新代理IP的状态为False(不可用)
                if data != {}:
                    db.update_proxy(proxy, False)
                else:
                    raise ValueError('Can\'t connect the website, please check your network!')
        '''
        r = requests.get(self.url, headers=headers, params=payload)
        r.encoding = 'utf-8'
        return r.text.encode('utf-8')

    def extract_result(self, results):
        print('Start extract goods info...')
        page = etree.HTML(results)
        # 先把列表抓取出来,再解析每项中的name, url, price
        goodses = page.xpath('//li[@class="s-result-item  celwidget "]')
        result_dict = {}
        for goods in goodses:
            try:
                goods_price = goods.xpath('div//span[contains(@class, "a-size-base a-color-price")][1]/text()')
                goods_name = goods.xpath('div/div[@class="a-row a-spacing-mini"][1]/div[1]/a/@title')
                goods_url = goods.xpath('div/div[@class="a-row a-spacing-mini"][1]/div[1]/a/@href')
                if not goods_price or not goods_url or not goods_price:
                    continue
                # 有些奇葩的亚马逊刊物定价'免费', 修正为0
                if goods_price[0].find(u'免费') != -1:
                    goods_price = float(0)
                else:
                    # 去掉价格上的¥符号, 替换,符号
                    # 某些amazon价格是一个范围'¥59 － ¥99', 需要只截取一部分
                    goods_price = float(goods_price[0][1:].replace(',', '').split('-')[0].strip())
                result_dict[goods_name[0]] = (goods_url[0], goods_price)
            except:
                # 出错就忽略继续解析下一个商品
                continue
        return result_dict

    def search(self, key_word, page_number=1):
        results = self.get_result(key_word, page_number)
        return self.extract_result(results)
