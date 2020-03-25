from collections import defaultdict
import dateutil.parser
import numpy as np
import matplotlib.pyplot as plt

# DJI.csv from Yahoo Finance
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
    series[key] = np.vectorize(callback)(series[key])

def percent_change(raw_data):
    return np.diff(raw_data) / np.array(raw_data[:-1 or None])

def plot_histogram(raw_data, raw_times, threshold=0.03, binwidth=0.001):
    dater = percent_change(raw_data)
    times = raw_times[np.abs(dater) > threshold]
    dater = dater[np.abs(dater) > threshold]
    print("sorted by times")
    for t, d in zip(times, dater):
        print(f"{100*d:.1f}% change on {t}")
    times = [t for _, t in sorted(zip(dater, times))]
    print("\nsorted by percentage")
    for t, d in zip(times, sorted(dater)):
        print(f"{100*d:.1f}% change on {t}")

    plt.hist(dater, bins=np.arange(np.min(dater), np.max(dater)+binwidth, binwidth))
    plt.show()


data = [data_dict(x, headers) for x in lines]
series = to_series(data)

convert_type(series, 'Open', float)
convert_type(series, 'Date', dateutil.parser.parse)

plot_histogram(series['Open'], series['Date'][1:])
