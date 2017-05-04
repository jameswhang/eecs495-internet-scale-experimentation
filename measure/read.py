from __future__ import division

import glob
import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy
import statsmodels
from statsmodels.distributions.empirical_distribution import ECDF

#matplotlib.use('png')

chrome_nonamp = 'measurement_chrome_non_amp2017_04_14'
firefox_nonamp = 'measurement_firefox_non_amp2017_04_13'
firefox_amp = 'measurement_firefox_amp2017_04_13'
chrome_amp = 'measurement_chrome_amp_2017_04_14'

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


def main():
    chrome_amp_data = []
    amp_data = []
    nonamp_data = []

    for line in open(chrome_amp, 'rb').readlines()[1:]:
        line = line.replace('\n', '')
        tokens = line.split(',')
        navigationStart = int(tokens[0])
        domainLookupStart = int(tokens[7])
        domainLookupEnd = int(tokens[8])
        loadEventEnd = int(tokens[len(tokens)-1])

        if loadEventEnd == 0:
            continue

        if loadEventEnd - navigationStart:
            loadTime = loadEventEnd - navigationStart
            dnsQueryTime = domainLookupEnd - domainLookupStart
            chrome_amp_data.append(loadTime - dnsQueryTime)


    for line in open(firefox_nonamp, 'rb').readlines()[1:]:
        line = line.replace('\n', '')
        tokens = line.split(',')
        navigationStart = int(tokens[0])
        domainLookupStart = int(tokens[7])
        domainLookupEnd = int(tokens[8])
        loadEventEnd = int(tokens[len(tokens)-1])

        if loadEventEnd == 0:
            continue

        if loadEventEnd > navigationStart:
            loadTime = loadEventEnd - navigationStart
            dnsQueryTime = domainLookupEnd - domainLookupStart
            nonamp_data.append(loadTime - dnsQueryTime)

    for line in open(firefox_amp, 'rb').readlines()[1:]:
        line = line.replace('\n', '')
        tokens = line.split(',')
        navigationStart = int(tokens[0])
        domainLookupStart = int(tokens[7])
        domainLookupEnd = int(tokens[8])
        loadEventEnd = int(tokens[len(tokens)-1])

        if loadEventEnd == 0:
            continue

        if loadEventEnd > navigationStart:
            loadTime = loadEventEnd - navigationStart
            dnsQueryTime = domainLookupEnd - domainLookupStart
            amp_data.append(loadTime - dnsQueryTime)

    print amp_data
    print chrome_amp_data
    print nonamp_data

    chrome_amp_linedata = ECDF(chrome_amp_data)
    amp_linedata = ECDF(amp_data)
    nonamp_linedata = ECDF(nonamp_data)

    plt.figure(figsize=(5.5,5.5))

    line1, = plt.plot(chrome_amp_linedata.x, chrome_amp_linedata.y, lw=3, label='Chrome AMP')
    line2, = plt.plot(amp_linedata.x, amp_linedata.y, lw=3, label='Firefox AMP')
    line3, = plt.plot(nonamp_linedata.x, nonamp_linedata.y, lw=3, label='Non AMP')
    plt.legend(handles=[line1, line2, line3], loc=2)
    plt.xlabel('Page loading time (ms)')
    plt.ylim(0,1)
    plt.ylabel('CDF')
    plt.xscale("log")
    plt.savefig("figs/performance-chrome-ff-plt.pdf", bbox_inches="tight")
    plt.savefig("figs/performance-chrome-ff-plt.png", bbox_inches="tight")
    plt.close()


if __name__ == '__main__':
    main()

