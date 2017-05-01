from __future__ import division

import glob
import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy
import statsmodels
from statsmodels.distributions.empirical_distribution import ECDF

chrome_nonamp = 'measurement_chrome_non_amp2017_04_13'
firefox_nonamp = 'measurement_firefox_non_amp2017_04_13'
firefox_amp = 'measurement_firefox_amp2017_04_13'
chrome_amp = 'measurement_chrome_amp_2017_04_13'

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
    amp_data = []
    nonamp_data = []

    amp_dns = []
    nonamp_dns = []

    amp_fb = []
    nonamp_fb = []

    for line in open(firefox_nonamp, 'rb').readlines()[1:]:
        line = line.replace('\n', '')
        tokens = line.split(',')
        navigationStart = int(tokens[0])
        loadEventEnd = int(tokens[len(tokens)-1])
        domainLookupStart = int(tokens[6])
        domainLookupEnd = int(tokens[7])
        requestStart = int(tokens[11])
        responseStart = int(tokens[12])

        if loadEventEnd > navigationStart:
            nonamp_data.append(loadEventEnd - navigationStart)

        if domainLookupEnd > domainLookupStart:
            nonamp_dns.append(domainLookupEnd-domainLookupStart)
        if responseStart > requestStart:
            nonamp_fb.append(responseStart - requestStart)

    for line in open(firefox_amp, 'rb').readlines()[1:]:
        line = line.replace('\n', '')
        tokens = line.split(',')
        domainLookupStart = int(tokens[6])
        domainLookupEnd = int(tokens[7])

        navigationStart = int(tokens[0])
        loadEventEnd = int(tokens[len(tokens)-1])

        requestStart = int(tokens[11])
        responseStart = int(tokens[12])

        if loadEventEnd > navigationStart:
            amp_data.append(loadEventEnd - navigationStart)
        if domainLookupEnd > domainLookupStart:
            amp_dns.append(domainLookupEnd-domainLookupStart)
        if responseStart > requestStart:
            amp_fb.append(responseStart - requestStart)

    amp_linedata = ECDF(amp_data)
    nonamp_linedata = ECDF(nonamp_data)

    plt.figure(figsize=(4,3))
    line1, = plt.plot(amp_linedata.x, amp_linedata.y, lw=3, label='AMP')
    line2, = plt.plot(nonamp_linedata.x, nonamp_linedata.y, lw=3, label='Non AMP')
    plt.legend(handles=[line1, line2], loc=2)
    plt.xlabel('Page loading time (ms)')
    plt.ylim(0,1)
    plt.ylabel('CDF')
    plt.xscale("log")
    plt.savefig("figs/performance-plt.pdf", bbox_inches="tight")
    plt.savefig("figs/performance-plt.png", bbox_inches="tight")

    """
    plt.figure(figsize=(4,3))
    line1, = plt.plot(amp_linedata.x, 1-amp_linedata.y, lw=3, label='AMP')
    line2, = plt.plot(nonamp_linedata.x, 1-nonamp_linedata.y, lw=3, label='Non AMP')
    plt.legend(handles=[line1, line2], loc=4)
    plt.xlabel('Load Time(ms)', fontsize=14)
    plt.ylabel('Cumulative Frequency', fontsize=14)
    plt.yscale('symlog', linthreshy=0.1)
    plt.yticks([0, .01, .1, .5, 1], ["1", ".99", ".9", ".5", "0"])
    #plt.yscale('log', linthreshy=0.1)
    #plt.yticks([.01, .1, .5, 1], [".99", ".9", ".5", "0"])
    plt.gca().invert_yaxis()
    plt.savefig("figs/performance-plt.log.pdf", bbox_inches="tight")
    """

    amp_linedata = ECDF(amp_dns)
    nonamp_linedata = ECDF(nonamp_dns)

    plt.figure(figsize=(4,3))
    line1, = plt.plot(amp_linedata.x, amp_linedata.y, lw=3, label='AMP')
    line2, = plt.plot(nonamp_linedata.x, nonamp_linedata.y, lw=3, label='Non AMP')

    # Create another legend for the second line.
    plt.legend(handles=[line1, line2], loc=4)
    plt.xlabel('Time for DNS Query(ms)')
    plt.ylim(0,1)
    plt.ylabel('CDF')
    plt.xscale("log")
    plt.savefig("figs/performance-dns.pdf", bbox_inches="tight")
    plt.savefig("figs/performance-dns.png", bbox_inches="tight")

    amp_linedata = ECDF(amp_fb)
    nonamp_linedata = ECDF(nonamp_fb)

    plt.figure(figsize=(4,3))
    line1, = plt.plot(amp_linedata.x, amp_linedata.y, lw=3, label='AMP')
    line2, = plt.plot(nonamp_linedata.x, nonamp_linedata.y, lw=3, label='Non AMP')

    # Create another legend for the second line.
    plt.legend(handles=[line1, line2], loc=4)
    plt.xlabel('Time to first byte (ms)')
    plt.ylabel('CDF')
    plt.ylim(0,1)
    plt.xscale("log")
    plt.savefig("figs/performance-fb.pdf", bbox_inches="tight")
    plt.savefig("figs/performance-fb.png", bbox_inches="tight")
    plt.close()


if __name__ == '__main__':
    main()

