from __future__ import division

import pprint
import time
import glob
import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy
import statsmodels
from statsmodels.distributions.empirical_distribution import ECDF

pp = pprint.PrettyPrinter(indent=4)
matplotlib.use('pdf')
AMP_SCRIPTS = ['preconnect.gif', 'amp-analytics-0.1.js', 'v0/amp-ad-0.1.js', 'v0.js', 'google/v9.js', 'v0/amp-iframe-0.1.js', 'amp-analytics-0.1.js', 'amp-iframe-0.1.js']

text_sizes = []
image_sizes = []
script_sizes = []
other_sizes = []
total_sizes = []

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


def read_pickle(picklefile):
    d = pickle.load(open(picklefile, 'rb'))
    entries = d[u'log'][u'entries']

    number_in = 0
    total_number = len(entries)

    time_initial = entries[0][u'startedDateTime']
    time_final = time_initial

    for entry in entries:
        size = entry[u'response'][u'bodySize']
        startDT = entry[u'startedDateTime'].split('T')[1].split('-')[0]
        time = entry[u'time']

        print startDT


pickles = glob.glob('./pickles/*.pickle')

for picklefile in pickles:
    read_pickle(picklefile)
    break


