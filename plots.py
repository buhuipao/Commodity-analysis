# _*_ coding: utf-8 _*_

from bokeh import plotting
from bokeh.resources import CDN
from bokeh import embed

import pandas as pd
from sklearn import linear_model

import time


def make_my_plot(data):
    prices = data['prices']
    title = u'价格走势图'
    # 转化时间20170301为时间戳，方便绘图
    x = map(lambda item: pd.tslib.Timestamp(str(item['date'])), prices)
    y = map(lambda item: item['price'], prices)
    predict_date, predict_price = get_predict(map(lambda item: item['date'], prices), y)
    tomorrow = pd.tslib.Timestamp(str(predict_date))
    x.append(tomorrow)
    y.append(predict_price)
    p = plotting.figure(
            title=title,
            plot_width=800,
            plot_height=250,
            x_axis_type="datetime",
            x_axis_label=u'日期',
            y_axis_label=u'价格')
    p.line(x, y, line_width=2)
    p.circle(x[:-1], y[:-1], fill_color="white", size=8)
    p.circle(x[-1:], y[-1:], fill_color="red", size=8)
    image = embed.file_html(p, CDN, u"标题").decode('utf-8')
    return image


def get_predict(dates, prices):
    # 利用回归线算法预测明天的价格
    # 输入([20170301, 20170302, ...], [1000, 900, 8000])
    # 输出(明日时间戳，预计价格)
    tomorrow = time.time() + 3600*24
    x_data = map(lambda date: [time.mktime(time.strptime(str(date), '%Y%m%d'))], dates)
    y_data = prices
    regr = linear_model.LinearRegression(x_data, y_data)
    regr.fit(x_data, y_data)
    predict_price = regr.predict(tomorrow)
    predict_date = time.strftime('%Y%m%d', time.localtime(tomorrow))
    return (predict_date, predict_price[0])
