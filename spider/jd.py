# _*_ coding: utf-8 _*_

import requests
import re
import sys
from lxml import etree
from ipdb import set_trace


class JD(object):
    '''
    JD爬虫的两个参数(price，key_word)来自Amazon的搜索结果，但是如何确定在Amazon获取到的商品（商品名）在JD能搜索到同一件商品
    我做了以下判断:
        1) 通过价格限制，因为两件商品在JD，Amazon的价格差距不会超过商品的10%，min_price <= price <= max_price
        2) 通过比较关键字，Amazon的关键字和JD结果的关键字与的结果, 结果的长度／JD商品关键字 >= 0.50
    '''
    def __init__(self, price, key_word):
        self.price = int(price)
        self.key_word = key_word

    def get_result(self, price, key_word):
        key_word_str = key_word.replace(' ', '%20')
        min_price = str(price * 0.9)
        max_price = str(price * 1.1)
        url = 'http://search.jd.com/search?keyword=' + key_word_str + '&enc=utf-8&ev=exprice_' + min_price + '-' + max_price
        print(url)
        headers = \
            {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6 \
                            AppleWebKit/537.36 (KHTML, like Gecko \
                            Chrome/54.0.2840.71 Safari/537.36',
             'Host': 'search.jd.com',
             'connection': 'keep-alive',
             'Accept': 'text/html,application/xhtml+xml,application/xml;\
                        q=0.9,image/webp,*/*;q=0.8',
             'Accept-Encoding': 'gzip, deflate, sdch',
             'Upgrade-Insecure-Requests': '1',
             'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
             'Content-Type': 'text/plain;charset=UTF-8'
             }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        return response.text.encode('utf-8')

    def extract_result(self, search_result):
        html = search_result
        page = etree.HTML(html)
        products_name = page.xpath('//ul[@class="gl-warp clearfix"]/li[@data-sku]/div/div[contains(@class, "p-name")]/a/@title')
        products_url = page.xpath('//ul[@class="gl-warp clearfix"]/li[@data-sku]/div/div[contains(@class, "p-name")]/a/@href')
        products_price = page.xpath('//ul[@class="gl-warp clearfix"]/li[@data-sku]/div/div[contains(@class, "p-price")]//i/text()')
        '''
        products_url.pop(4)
        products_name.pop(4)
        '''
        self.clean_Ad(products_url, products_name)
        # 给连接添加'https://'头
        make_url = lambda url: url.replace('//', 'https://')
        products_url = map(make_url, products_url)
        for i in xrange(len(products_name)):
            print(products_name[i])
            print(products_price[i])
            print(products_url[i])
        return (products_name, products_price, products_url)

    # 去除jd广告推荐商品的url同时去掉商品列表中对应的商品名, 之前价格解析不到所以不需要做去除操作
    def clean_Ad(self, urls, names):
        for url in urls:
            if url.find('https://') != -1:
                index = urls.index(url)
                urls.pop(index)
                names.pop(index)

    def verify_name(self, a_name, j_name):
        # 分割商品名得到集合
        j_set = set(re.split(r'\s*[()（）+＋:： ]\s*', j_name))
        a_set = set(re.split(r'\s*[()（）+＋:： ]\s*', a_name))
        same_set = j_set & a_set
        if float(len(same_set)) / float(len(a_set)) >= 0.5:
            return True
        else:
            return False

    def run(self):
        page = self.get_result(self.price, self.key_word)
        return self.extract_result(page)

if __name__ == '__main__':
    jd = JD(sys.argv[1], sys.argv[2])
    jd.run()
