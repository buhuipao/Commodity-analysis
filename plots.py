# _*_ coding: utf-8 _*_

from bokeh import plotting
from bokeh.resources import CDN
from bokeh import embed


def make_my_plot(data):
    prices = data['prices']
    title = u'价格走势图'
    x = map(lambda price: price['date'], prices)
    y = map(lambda price: price['price'], prices)
    p = plotting.figure(title=title, plot_width=800, plot_height=250, x_axis_label=u'日期', y_axis_label=u'价格')
    p.line(x, y, legend="Price", line_width=2)
    p.circle(x, y, fill_color="white", size=8)

    image = embed.file_html(p, CDN, u"标题").decode('utf-8')
    return image
