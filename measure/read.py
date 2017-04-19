from __future__ import division

import glob
import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy
import statsmodels
from statsmodels.distributions.empirical_distribution import ECDF


CA = open('measurement_chrome_amp_2017_04_14', 'rb').readlines()
CN = open('measurement_chrome_non_amp2017_04_14', 'rb').readlines()
FA = open('measurement_firefox_amp2017_04_14', 'rb').readlines()
FN = open('measurement_firefox_non_amp2017_04_14', 'rb').readlines()

keys = ['navigationStart', 'unloadEventStart', 'unloadEventEnd', 'redirectStart', 'redirectEnd', 'fetchStart', 'domainLookupStart', 'domainLookupEnd', 'connectStart', 'connectEnd', 'secureConnectionStart', 'requestStart', 'responseStart', 'responseEnd', 'domLoading', 'domInteractive', 'domContentLoadedEventStart', 'domComplete', 'loadEventStart', 'loadEventEnd']

CA_loadtimes = []
CN_loadtimes = []
FA_loadtimes = []
FN_loadtimes = []

def make_cdf(data, label, filename):
    # I found both of these in my script, not sure what the difference was,
    # might be slightly different.
    #linedata = statsmodels.tools.tools.ECDF(data) #linedata = ECDF(data)
    linedata = ECDF(data)


    plt.figure(figsize=(5.5,5.5))
    plt.plot(linedata.x, linedata.y, lw=3, label=label)
    plt.xlabel('Bytes(KB)', fontsize=14)
    plt.ylabel('Cumulative Frequency', fontsize=14)

    plt.savefig(filename+".pdf", bbox_inches="tight")
    plt.close()


for line in CA[1:]:
    line = line.replace('\n', '')
    times = line.split(',')
    t = int(times[19]) - int(times[0])
    if t < 0: 
        continue
    CA_loadtimes.append(t)

for line in CN[1:]:
    line = line.replace('\n', '')
    times = line.split(',')
    t = int(times[19]) - int(times[0])
    if t < 0: 
        continue
    CN_loadtimes.append(t)

for line in FA[1:]:
    line = line.replace('\n', '')
    times = line.split(',')
    t = int(times[19]) - int(times[0])
    if t < 0: 
        continue
    FA_loadtimes.append(t)

for line in FN[1:]:
    line = line.replace('\n', '')
    times = line.split(',')
    t =int(times[19]) - int(times[0])
    if t < 0: 
        continue
    FN_loadtimes.append(t)

make_cdf(CA_loadtimes, 'Average size of prefetched AMP data on Mobile Browser', 'Total Size')
make_cdf(CN_loadtimes, 'Average size of prefetched AMP data on Mobile Browser', 'Total Size')

