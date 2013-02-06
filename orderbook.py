import numpy as np
import pandas as pd
from matplotlib.dates import date2num
import generate_test_data

def build_array(prices, tick=0.1):
    dt = pd.Series(prices.index.to_pydatetime()).diff().dropna().min()
    dtt = dt.microseconds/1000 if dt.seconds == 0 else dt.seconds
    mi = pd.Series(prices.index.to_pydatetime()).min()
    mx = pd.Series(prices.index.to_pydatetime()).max()
    xlen = ((mx-mi).total_seconds()/dtt)*(1000 if dt.seconds==0 else 1) + 1
    ylen = int(round((prices.max().max()-prices.min().min())/tick))
    
    return np.zeros((xlen,ylen))/0., prices.min().min(), prices.max().max()

def calc_price_y(op, miny, tick=0.1):
    return op.applymap(lambda x:(x-miny)/tick)

def resample_x(op):
    dt = pd.Series(op.index.to_pydatetime()).diff().dropna().min()
    dtt = str(dt.microseconds/1000)+'L' if dt.seconds == 0 else str(dt.seconds)+'S'
    tmp = op.resample(dtt,fill_method='pad')
    tmp['idx'] = 1
    tmp['idx'] = tmp.idx.cumsum()
    return tmp

def fill_array(x, arr, qtys):
    try:
        for i in list(x.iteritems())[:-1]:
            arr[x.ix['idx']-1,i[1]] = qtys.ix[x.name][i[0]]
    except Exception as e:
         import pdb;pdb.set_trace()


def test_data_ob():
    op = generate_test_data.generate_levels(generate_test_data.generate_price_plot(points = 100))
    qtys = generate_test_data.generate_qty_data(points = 100, index = op.index)
    arr, miny, maxy = build_array(op)
    op = resample_x(calc_price_y(op,miny))
    qtys = resample_x(qtys)
    op.apply(lambda x: fill_array(x, arr, qtys), axis=1)
    import pdb;pdb.set_trace()
    return arr, (date2num(op.index.to_pydatetime().min()), date2num(op.index.to_pydatetime().max()), miny, maxy)
