# _*_coding: utf-8 _*_

import re
import requests
from lxml import etree


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
        r.encoding = 'utf-8'
        return r.text.encode('utf-8')

    def extract_result(self, results):
        print('Start extract goods info...')
        page = etree.HTML(results)
        # 抽取li标签下的孙div标签的第一个子标签的a标签的title
        products_name = page.xpath('//li/div/div[@class="a-row a-spacing-mini"][1]/div[1]/a/@title')
        products_url = page.xpath('//li/div/div[@class="a-row a-spacing-mini"][1]/div[1]/a/@href')
        # 匹配第一页的每一项的第一个价格，解决了用xpath解析的BUG（不同种类商品搜索结构页面具有不同的结构, 导致一些商品价格解析不出）
        pattern = re.compile(r'<li id="result_.*?<span class="a-size-base a-color-price.*?">(.*?)</span>', re.S)
        products_price = re.findall(pattern, results)
        self.clean_Ad(products_url, products_name, products_price)
        print(len(products_url), len(products_name), len(products_price))
        return (products_name, products_price[:len(products_name)], products_url)

    def search(self, key_word, page_number=1):
        results = self.get_result(key_word, page_number)
        return self.extract_result(results)

    # 去掉广告项(广告项url不含https://, 以/gp/开头)
    def clean_Ad(self, urls, names, prices):
        for url in urls:
            if url.find('/dp/') == -1:
                print('Clean Ad goods...')
                index = urls.index(url)
                urls.pop(index)
                names.pop(index)
                prices.pop(index)
