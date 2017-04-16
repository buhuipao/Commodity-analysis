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
    # 转化时间(20170301)为时间戳，方便绘图, 图形展示更加友好
    x = map(lambda item: pd.tslib.Timestamp(str(item['date'])), prices)
    y = map(lambda item: item['price'], prices)
    # 得到预测的日期和价格
    predict_date, predict_price = get_predict(map(lambda item: item['date'], prices), y)
    tomorrow = pd.tslib.Timestamp(str(predict_date))
    x.append(tomorrow)
    y.append(predict_price)
    # 把所有时间和价格数据进行画图
    p = plotting.figure(
            title=title,
            # 定义画布的宽度、高度、横轴、纵轴
            plot_width=800,
            plot_height=250,
            x_axis_type="datetime",
            x_axis_label=u'日期',
            y_axis_label=u'价格')
    # 定义线的宽度为2个像素
    p.line(x, y, line_width=2)
    # 定义点的填充颜色为白色
    p.circle(x[:-1], y[:-1], fill_color="white", size=8)
    # 定义预测点的填充颜色为红色
    p.circle(x[-1:], y[-1:], fill_color="red", size=8)
    # 定义图像的标题
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
