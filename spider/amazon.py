# _*_coding: utf-8 _*_

import sys
import re
import requests
from lxml import etree


class Amazon(object):
    def __init__(self, key_word):
        self.key_word = key_word
        self.url = 'https://www.amazon.cn/s/ref=nb_sb_noss_1'

    def get_result(self, url, key_word):
        url = url + '?field-keywords=' + key_word
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
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        return r.text.encode('utf-8')

    def extract_result(self, results):
        page = etree.HTML(results)
        # 抽取li标签下的孙div标签的第一个子标签的a标签的title
        products_name = page.xpath('//li/div/div[3]/div[1]/a/@title')
        products_url = page.xpath('//li/div/div[3]/div[1]/a/@href')
        # 匹配第一页的每一项的第一个价格，解决了用xpath解析的BUG（不同种类商品搜索结构页面具有不同的结构, 导致一些商品价格解析不出）
        pattern = re.compile(r'<li id="result_.*?<span class="a-size-base a-color-price.*?">(.*?)</span>', re.S)
        products_price = re.findall(pattern, results)
        for i in xrange(len(products_url)):
            print("%s  %s  %s\n" % (products_name[i], products_price[i].decode('utf-8'), products_url[i]))

    def search(self):
        results = self.get_result(self.url, self.key_word)
        self.extract_result(results)

def run():
    key_word = sys.argv[1]
    amazon = Amazon(key_word)
    amazon_result = amazon.search()
    print(amazon_result)

if __name__ == '__main__':
    run()
