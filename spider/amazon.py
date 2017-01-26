# _*_coding: utf-8 _*_

import requests
from lxml import etree
from ipdb import set_trace


class Amazon(object):
    def __init__(self):
        self.url = 'https://www.amazon.cn/s/ref=sr_pg_1'

    def get_result(self, key_word, page_number):
        print('Start search goods...')
        headers = \
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6 \
                            AppleWebKit/537.36 (KHTML, like Gecko \
                            Chrome/54.0.2840.71 Safari/537.36',
             'Host': 'www.amazon.cn',
             'Accept': 'text/html,application/xhtml+xml,application/xml;\
                        q=0.9,image/webp,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate, sdch, br',
             'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6'
             }
        payload = {'ie': 'UTF8', 'keywords': key_word, 'page': page_number}
        r = requests.get(self.url, headers=headers, params=payload)
        print(r.url)
        r.encoding = 'utf-8'
        return r.text.encode('utf-8')

    def extract_result(self, results):
        print('Start extract goods info...')
        page = etree.HTML(results)
        # 先把列表抓取出来,再解析每项中的name, url, price
        goodses = page.xpath('//li[@class="s-result-item  celwidget "]')
        name_list, url_list, price_list = [], [], []
        for goods in goodses:
            goods_price = goods.xpath('div//span[contains(@class, "a-size-base a-color-price")][1]/text()')
            goods_name = goods.xpath('div/div[@class="a-row a-spacing-mini"][1]/div[1]/a/@title')
            goods_url = goods.xpath('div/div[@class="a-row a-spacing-mini"][1]/div[1]/a/@href')
            if not goods_price or not goods_url or not goods_price:
                continue
            name_list.append(goods_name[0])
            url_list.append(goods_url[0])
            price_list.append(goods_price[0])
        return (name_list, url_list, price_list)

    def search(self, key_word, page_number=1):
        results = self.get_result(key_word, page_number)
        return self.extract_result(results)
