# _*_ coding: utf-8 _*_

import jieba
import jieba.analyse

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
        a_spider.search(key_word, number)
        goods_names, goods_urls, goods_prices = a_spider.search(key_word, number)
        for i in xrange(len(goods_urls)):
            print(goods_names[i])
            print(goods_prices[i])
            print(goods_urls[i])


def extract_tags(key_word, a_name):
    '''
    根据商品名分词取前十个, 利用分析模块解析出关键字,提取相同部分,
    最后并集得出应该在JD搜索的关键字, 关键字数量不应该超过6个避免搜索结果出不来,
    针对搜索的商品名字类别，可以添加自定义词典提高准确度
    '''
    cut_tags = [tag for tag in jieba.cut(a_name)][:8]
    analyse_tags = jieba.analyse.extract_tags(a_name)
    tags = [tag for tag in cut_tags if tag in analyse_tags]
    # 把亚马逊搜索的关键字拼接到tags第一位
    try:
        tags.remove(key_word)
    except:
        pass
    tags.insert(0, key_word)
    if len(tags) > 5:
        tags = tags[:5]
    return ' '.join(tags)


if __name__ == '__main__':
    main()
