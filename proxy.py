# _*_coding: utf-8 _*_

import requests
import random
from lxml import etree
import threading
import time

from configs import USER_AGENTS
from sql import db

# from ipdb import set_trace


def Proxy(result, page):
    '''
    返回[{IP, PORT}, ...]
    '''
    url = 'http://www.xicidaili.com/nn/' + str(page)
    headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Encoding': 'gzip, deflate, lzma, sdch',
            'Accept': 'text/html,application/xhtml+xml,application/xml;\
                    q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.xicidaili.com'
            }
    # r = requests.get(url, headers=headers, proxies={'http': 'http://211.143.45.216:3128'}, timeout=10)
    while True:
        # 假设代理库里有可用代理，否则就采用本机IP为代理
        proxy = random.choice(db.find_porxy()) \
                if len(db.find_porxy()) != 0 else None
        if proxy:
            data = {'http': 'http://'+proxy['ip']+':'+proxy['port'],
                    'https': 'http://'+proxy['ip']+':'+proxy['port']}
        else:
            data = {}
        print(data, 'get xici...')
        try:
            r = requests.get(url, headers=headers, proxies=data, timeout=10)
            # 503状态码是西刺封IP的状态码，证明代理可用但被西刺已封, 不影响其他代理网站
            if r.status_code == 200 or r.status_code == 503:
                break
        except:
            # 如果用的本机IP访问就检查网络, 否则就更新数据库里的状态为False
            if data != {}:
                db.update_proxy(proxy, False)
            else:
                raise ValueError('Can\'t connect the website, please check your network!')
    try:
        page = etree.HTML(r.text.encode('utf-8'))
        items = page.xpath('//tr')
        for item in items:
            ip = item.xpath('td[2]/text()')
            port = item.xpath('td[3]/text()')
            ip_type = item.xpath('td[6]/text()')
            speed = item.xpath('td[7]/div/div/@class')
            if not ip or not port or \
                    speed[0] != 'bar_inner fast' or ip_type[0].find('socks') != -1:
                continue
            result.append({'ip': ip[0], 'port': port[0]})
    except:
        # 遇到西刺503的状态码直接滤过
        pass
    return result


def Check(proxies, action):
    url = 'http://www.buhuipao.com'
    headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Encoding': 'gzip, deflate, lzma, sdch',
            'Accept': 'text/html,application/xhtml+xml,application/xml;\
                q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'www.buhuipao.com'
            }
    for proxy in proxies:
        data = {'http': 'http://'+proxy['ip']+':'+proxy['port'],
                'https': 'http://'+proxy['ip']+':'+proxy['port']}
        if action == 'grab':
            try:
                r = requests.get(url, headers=headers, proxies=data, timeout=10)
            except Exception as e:
                continue
            if r.status_code == 200:
                db.update_proxy(proxy, True)
        else:
            try:
                r = requests.get(url, headers=headers, proxies=data, timeout=10)
            except Exception as e:
                db.update_proxy(proxy, False)
                continue
            if r.status_code != 200:
                db.update_proxy(proxy, False)


def catch_new_proxy():
    # 多线程检测爬取的代理IP, 设置代理的状态为可用
    results = []
    for page in xrange(1, 3):
        Proxy(results, page)
    # 如果返回空值直接返回
    if not results:
        return
    print('Start checkup newProxy...')
    t = len(results) / 10 if len(results) >= 10 else 1
    Threads = []
    for proxies in list(results[i:i+t] for i in xrange(0, len(results), t)):
        Threads.append(threading.Thread(target=Check, args=(proxies, 'grab',)))
    for Thread in Threads:
        Thread.start()
    for Thread in Threads:
        Thread.join()


def check_old_proxy():
    # 多线程检验从数据库查询的旧的代理，在查询前数据库还清理了不可用的代理
    # 检验过程中同时更新代理的状态
    results = db.find_porxy()
    t = len(results) / 6 if len(results) >= 6 else 1
    Threads = []
    for proxies in list(results[i:i+t] for i in xrange(0, len(results), t)):
        Threads.append(threading.Thread(target=Check, args=(proxies, 'check',)))
    for Thread in Threads:
        Thread.start()
    for Thread in Threads:
        Thread.join()


def run():
    while True:
        print('Start check old proxy...')
        check_old_proxy()

        print('Start sleep...')
        time.sleep(60)

        print('Start grab proxy...')
        catch_new_proxy()

        print('Start sleep...')
        time.sleep(60)


if __name__ == '__main__':
    run()
