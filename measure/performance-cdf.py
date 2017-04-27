from __future__ import division

import glob
import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy
import statsmodels
from statsmodels.distributions.empirical_distribution import ECDF

matplotlib.use('pdf')

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

    for line in open(firefox_nonamp, 'rb').readlines()[1:]:
        line = line.replace('\n', '')
        tokens = line.split(',')
        navigationStart = int(tokens[0])
        loadEventEnd = int(tokens[len(tokens)-1])

        if loadEventEnd > navigationStart:
            nonamp_data.append(loadEventEnd - navigationStart)

    for line in open(firefox_amp, 'rb').readlines()[1:]:
        line = line.replace('\n', '')
        tokens = line.split(',')
        navigationStart = int(tokens[0])
        loadEventEnd = int(tokens[len(tokens)-1])

        if loadEventEnd > navigationStart:
            amp_data.append(loadEventEnd - navigationStart)

    amp_linedata = ECDF(amp_data)
    nonamp_linedata = ECDF(nonamp_data)

    plt.figure(figsize=(5.5,5.5))
    line1, = plt.plot(amp_linedata.x, amp_linedata.y, lw=3, label='AMP')
    line2, = plt.plot(nonamp_linedata.x, nonamp_linedata.y, lw=3, label='Non AMP')

    # Create a legend for the first line.
    first_legend = plt.legend(handles=[line1], loc=1)

    ax = plt.gca().add_artist(first_legend)

    # Create another legend for the second line.
    plt.legend(handles=[line2], loc=4)
    plt.xlabel('Load Time(ms)', fontsize=14)
    plt.ylabel('Cumulative Frequency', fontsize=14)
    plt.savefig("performance-1.pdf", bbox_inches="tight")
    plt.close()


if __name__ == '__main__':
    main()

