# _*_ coding: utf-8 _*_

import jieba
import jieba.analyse
import time

from spider import jd
from spider import amazon
from ipdb import set_trace


def main():
    # 如果输入两个字符则表示限制最低搜索价格
    Input = raw_input('Please enter product name\n').strip().split()
    if len(Input) == 0:
        print('WARNING: Goods name should not be none!')
        return
    elif len(Input) > 2:
        print('WAENING: The wrong format of the goods you provided!')
        return
    else:
        key_word = Input[0].decode('utf-8')
        try:
            limit_price = float(Input[1])
        except:
            print('WARNING: Please provide the correct price limit or provide the correct price format!')
            return

    a_spider = amazon.Amazon()
    j_spider = jd.JD()
    try:
        page_number = int(raw_input('Please enter the number of pages you want to search\n').strip())
    except:
        page_number = 1
    for number in xrange(1, page_number+1):
        a_results = a_spider.search(key_word, number)
        for name in a_results.keys():
            search_word = extract_tags(key_word, name)
            assert type(a_results[name][-1]) == float
            if a_results[name][-1] < limit_price:
                continue
            print(search_word)
            print(name, a_results[name][0], a_results[name][-1])
            try:
                j_results = j_spider.search(a_results[name][-1], search_word)
                # 如果搜索不到尝试反转搜索关键词
                if len(j_results) == 0:
                    j_results = j_spider.search(a_results[name][-1], ' '.join(search_word.split()[::-1]))
                for result in chose_result(a_results[name][-1], j_results):
                    print(result)
                print('\n\n')
            except Exception as e:
                print(e)
                continue


def extract_tags(key_word, a_name):
    '''
    根据商品名分词取前十个, 利用分析模块解析出关键字,提取相同部分,
    最后并集得出应该在JD搜索的关键字, 关键字数量不应该超过5个避免搜索结果出不来,
    针对搜索的商品名字类别，可以添加自定义词典提高准确度（后再加）
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


def chose_result(a_price, j_results):
    assert type(j_results) == dict
    # 对结果字典按照value进行排序
    j_results = sorted(j_results.items(), key=lambda item: item[1][1])
    if len(j_results) >= 2:
        for result in j_results:
            if result[1][1] >= a_price:
                return (j_results[0], result)
    elif len(j_results) == 1:
        return j_results[0]
    else:
        return {}

if __name__ == '__main__':
    main()
