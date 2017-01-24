# _*_ coding: utf-8 _*_

import sys
import logging
from spider import jd, amazon


def main():
    # 如果输入两个字符则表示限制搜索价格
    Input = raw_input('Please enter product name\n').strip().split()
    if len(Input) == 0:
        print('WARNING: Goods name should not be none!')
        return
    elif len(Input) == 1:
        key_word = Input[0]
        price = None
    elif len(Input) == 2:
        key_word = Input[0]
        try:
            price = int(Input[1])
        except:
            print('ERROR: The wrong format of the goods price you provided!')
    else:
        print('WAENING: The wrong format of the goods you provided!')
        return

    a_spider = amazon.Amazon()
    try:
        page_number = int(raw_input('Please enter the number of pages you want to search\n').strip())
    except:
        pass
    for number in xrange(1, page_number+1):
        products_name, products_price, products_url = a_spider.search(key_word, number)
        for i in xrange(len(products_url)):
            print(products_name[i], products_price[i], products_url[i])

if __name__ == '__main__':
    main()
