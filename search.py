# _*_ coding: utf-8 _*_

import jieba
import jieba.analyse

from spider import jd
from spider import amazon
from sql import db
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
            limit_price = float(0)

    a_spider = amazon.Amazon()
    j_spider = jd.JD()
    try:
        page_number = int(raw_input('Please enter the number of pages you want to search\n').strip())
    except:
        page_number = 1

    for number in xrange(1, page_number+1):
        # Amazon爬虫返回的结果格式为一个字典，像这样{A_name: (A_url, A_price), B_name: (B_url, B_price), ...}
        a_results = a_spider.search(key_word, number)
        for name in a_results.keys():
            search_word = extract_tags(key_word, name)
            assert type(a_results[name][1]) == float
            # 筛选用户大于设定价格的的商品，如果价格小于设定的价格就忽略
            if a_results[name][1] < limit_price:
                continue
            try:
                # 以Amazon的商品价格作为期望价格(0.9~1.1)做限定价格去搜索JD商品
                j_results = j_spider.search(a_results[name][-1], search_word)
                # 如果搜索不到尝试反转搜索关键词
                if len(j_results) == 0:
                    j_results = j_spider.search(a_results[name][1], ' '.join(search_word.split()[::-1]))
                same_goods = chose_result(a_results[name][1], j_results)
                data = {'name': name, 'key_word': search_word, 'url': a_results[name][0], 'price': a_results[name][1], 'same': same_goods}
                db.save_result(data)
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
    assert type(a_price) == float
    assert type(j_results) == dict
    '''
    对结果字典按照value进行排序
    如果结果长度大于二，则返回最低价和第一个大于等于amazon价格的结果项的列表
    否则返回空列表
    '''
    results = sorted(j_results.items(), key=lambda item: item[1][1])
    # 目标项的格式(name, (url, price)), 取得目标项组成字典列表存到mongoDB
    if len(results) >= 2:
        min_result = results[0]
        gt_result = [result for result in results if result[1][1] >= a_price][0]
        one_list = [{'j_name': min_result[0], 'url': min_result[1][0], 'price': min_result[1][1]}]
        two_list = [{'j_name': min_result[0], 'url': min_result[1][0], 'price': min_result[1][1]},
                    {'j_name': gt_result[0], 'url': gt_result[1][0], 'price': gt_result[1][1]}]
        if not gt_result:
            return one_list
        elif gt_result == min_result:
            return one_list
        else:
            return two_list
    elif len(results) == 1:
        return one_list
    else:
        return []


if __name__ == '__main__':
    main()
