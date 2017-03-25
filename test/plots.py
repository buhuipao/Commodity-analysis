# _*_ coding: utf-8 _*_

from ipdb import set_trace

import pandas as pd
from bokeh.plotting import figure, output_file, show

AAPL = pd.read_csv(
        '/Users/chenhua/Downloads/table.csv',
        parse_dates=['Date']
    )

output_file("datetime.html")

set_trace()
# create a new plot with a datetime axis type
p = figure(width=800, height=250, x_axis_type="datetime")

p.line(AAPL['Date'], AAPL['Close'], color='navy', alpha=0.5)

show(p)
