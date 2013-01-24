import pandas
import random
import numpy as np

def generate_price_plot(points=10000, p0=99.25, tick = 0.1):
    """Generate some random price data
    I am being quite verbose (lazy)
    """
    df = pandas.DataFrame({'x':[random.randint(0,3) for i in range(points)]})
    df['change'] = df.x.map(lambda x: 0 if x<2 else 1)
    df['change'] = df.change * df.x.map(lambda x: 1 if x<3 else -1)
    df['change'] = df.change * tick
    return (df.change.cumsum()+p0)


def generate_levels(mid, depth=5, tick=0.1):
    """Generate price leves
    Makes naive assumption that levels are 1 tick apart
    """
    ask = dict([(i+1,mid+i*tick) for i in range(depth)])
    bid = dict([( -i,mid-i*tick) for i in range(1,depth+1)])
    ask.update(bid)
    return pandas.DataFrame(ask)

def generate_qty_data(points=10000, depth=5, maxSize=120):
    df = pandas.DataFrame(dict([(i,np.random.randint(maxSize,size=points)) for i in range(depth*2)]))
    df.columns = range(-depth,0)+range(1,depth)
    return df
