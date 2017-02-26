# _*_ coding: utf-8 _*_

import requests
from lxml import etree
from ipdb import set_trace


class JD(object):
    '''
    JD爬虫的两个参数(price，key_word)来自Amazon的搜索结果，但是如何确定在Amazon获取到的商品（商品名）在JD能搜索到同一件商品
    我做了以下判断:
        1) 通过价格限制，因为两件商品在JD，Amazon的价格差距不会超过商品的10%，min_price <= price <= max_price
        2) 通过比较关键字，Amazon的关键字和JD结果的关键字与的结果, 结果的长度／JD商品关键字 >= 0.50
    '''
    def __init__(self):
        self.url = 'http://search.jd.com/search'

    def get_result(self, price, key_word):
        key_word_str = key_word
        min_price = str(float(price) * 0.9)
        max_price = str(float(price) * 1.1)
        price_limit = 'exprice_' + min_price + '-' + max_price
        payload = {'keyword': key_word_str, 'enc': 'utf-8', 'ev': price_limit}
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
        response = requests.get(self.url, headers=headers, params=payload, timeout=60)
        response.encoding = 'utf-8'
        return response.text.encode('utf-8')

    def extract_result(self, html):
        page = etree.HTML(html)
        products_name = []
        # 如果搜索不到结果，则解析jd推荐结果
        if html.find('class="notice-search"') != -1:
            names = page.xpath("string(//ul[@class='clearfix'][1]/li/div/div[@class='p-name']//em)")
            for name in names:
                products_name.append(name.xpath('string(.)'))
            products_url = page.xpath('//ul[@class="clearfix"][1]/li/div/div[@class="p-name"]/a/@href')
            products_price = page.xpath('//ul[@class="clearfix"][1]/li/div/div[@class="p-price"]//i/text()')
        else:
            names = page.xpath("//ul[@class='gl-warp clearfix']/li[@data-sku]/div/div[contains(@class, 'p-name')]/a/em")
            for name in names:
                products_name.append(name.xpath('string(.)'))
            products_url = page.xpath('//ul[@class="gl-warp clearfix"]/li[@data-sku]/div/div[contains(@class, "p-name")]/a/@href')
            products_price = page.xpath('//ul[@class="gl-warp clearfix"]/li[@data-sku]/div/div[contains(@class, "p-price")]//i/text()')
        # 如果解析不正确返回空字典
        if not products_name or not products_url or not products_price:
            return {}
        self.clean_Ad(products_url, products_name)

        # 给链接添加'https://'头
        make_url = lambda url: url.replace('//', 'https://')
        products_url = map(make_url, products_url)
        result_dict = {}
        for i in xrange(len(products_name)):
            result_dict[products_name[i]] = (products_url[i], float(products_price[i]))
        return result_dict

    # 去除jd广告推荐商品的url同时去掉商品列表中对应的商品名, 之前价格解析不到所以不需要做去除操作
    def clean_Ad(self, urls, names):
        for url in urls:
            if url.find('https://') != -1:
                index = urls.index(url)
                urls.pop(index)
                names.pop(index)

    def search(self, price, key_word):
        page = self.get_result(price, key_word)
        return self.extract_result(page)
