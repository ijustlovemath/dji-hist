from collections import defaultdict
import dateutil.parser
import numpy as np
import matplotlib.pyplot as plt

with open('DJI.csv', 'r') as f:
    lines = f.readlines()
    lines = [l.rstrip('\r\n') for l in lines]

headers = lines.pop(0).split(',')

def data_dict(line, headers):
    d = {}
    for x, h in zip(line.split(','), headers):
        d[h] = x
    return d

def to_series(data):
    s = defaultdict(list)
    for d in data:
        for k, v in d.items():
            s[k].append(v)
    return s

def convert_type(series, key, callback):
    series[key] = list(map(callback, series[key]))

def percent_change(series, key):
    return np.diff(series[key]) / np.array(series[key][:-1 or None])

def plot_histogram(series, key, binwidth=0.001):
    dater = percent_change(series, key)
    plt.hist(dater, bins=np.arange(np.min(dater), np.max(dater)+binwidth, binwidth))
    plt.show()


data = [data_dict(x, headers) for x in lines]
series = to_series(data)

convert_type(series, 'Open', float)
convert_type(series, 'Date', dateutil.parser.parse)

plot_histogram(series, 'Open')
