from __future__ import division

import json
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

def make_cdf(amp_data, nonamp_data, filename, ylabel):
    # I found both of these in my script, not sure what the difference was,
    # might be slightly different.
    plt.figure(figsize=(5.5,5.5))

    '''
    for i in range(len(amp_data) - 1):
        plt.plot([amp_data[i][0], amp_data[i][1]], [amp_data[i+1][0], amp_data[i+1][1]], 'k-', lw=3)

    for i in range(len(nonamp_data) - 1):
        plt.plot([nonamp_data[i][0], nonamp_data[i][1]], [nonamp_data[i+1][0], nonamp_data[i+1][1]], 'k-', lw=3)
    '''

    amp_data_x = [tup[0] for tup in amp_data]
    amp_data_y = [tup[1] for tup in amp_data]

    nonamp_data_x = [tup[0] for tup in nonamp_data]
    nonamp_data_y = [tup[1] for tup in nonamp_data]

    line1, = plt.plot(amp_data_x, amp_data_y, marker='o', color='r', label='AMP')
    line2, = plt.plot(nonamp_data_x, nonamp_data_y, marker='o', color='b', label='Non AMP')

    '''
    for tup in amp_data:
        plt.plot(tup[0], tup[1], lw=3, marker='o', markersize=3, color="red", label="AMP")
    for tup in nonamp_data:
        plt.plot(tup[0], tup[1], lw=3, marker='o', markersize=3, color="blue", label="Non AMP")
    '''
    plt.legend(handles=[line1, line2], loc=4)

    plt.xlabel('Time(s)', fontsize=14)
    plt.ylabel(ylabel, fontsize=14)

    plt.savefig("{}.png".format(filename), bbox_inches="tight")
    plt.close()


def parse_time(time_str):
    #print time_str
    startDT = time_str.split('T')[1].replace('Z', '').split('-')[0]
    minute = int(startDT.split(':')[-2])
    seconds = float(startDT.split(':')[-1])
    return minute * 60 + seconds

def read_pickle(picklefile, is_amp):
    with open(picklefile, 'rb') as pickle_file:
        d = pickle.load(pickle_file)

    entries = d[u'log'][u'entries']

    cum_number_in = 0
    total_number = len(entries)

    time_initial = parse_time(entries[0][u'startedDateTime'])
    time_final = time_initial

    size_data = []
    dns_data = []
    data = []

    total_size = 0
    cum_size = 0

    urls = []

    for entry in entries:
        total_size += entry[u'response'][u'bodySize']
        url = entry[u'request'][u'url']
        domains =  url.split('/')[2].split('.')
        if domains[-1] == 'com' or domains[-1] == 'net':
            domain = domains[-2] + '.' + domains[-1]
        else:
            domain = url.split('/')[2]
        
        if domain not in urls:
            urls.append(domain)
    

    for entry in entries:
        cum_number_in += 1
        size = entry[u'response'][u'bodySize']
        cum_size += size
        start = parse_time(entry[u'startedDateTime'])
        time = entry[u'time'] / 1000
        endtime = start + time
        size_data.append((endtime-time_initial, size))

    total_num = len(size_data)
    size_data_sorted = sorted(size_data, key=lambda tup: tup[0])
    size_over_time = []

    cum_size = 0
    cum_num = 0

    for size_data in size_data_sorted:
        cum_size += size_data[1]
        cum_num += 1
        size_over_time.append((size_data[0], cum_size/total_size))
        data.append((size_data[0], cum_num/total_num))

    return data, size_over_time, urls

amp_pickles = glob.glob('./amp_pickles/*.pickle')
nonamp_pickles = glob.glob('./nonamp_pickles/*.pickle')

assert len(amp_pickles) == len(nonamp_pickles)


amp_dns_lens = []  # Number of Domain resolutions to be made for AMP
nonamp_dns_lens = []  # Number of Domain resolutions to be made for Non AMP

for i in range(len(amp_pickles)):
    amp = amp_pickles[i]
    nonamp = nonamp_pickles[i]

    amp_data, amp_size, amp_domains = read_pickle(amp, True)
    nonamp_data, nonamp_size, nonamp_domains = read_pickle(nonamp, False)

    amp_dns_lens.append(len(amp_domains))
    nonamp_dns_lens.append(len(nonamp_domains))

    #make_cdf(amp_data, nonamp_data, './figs/num_obj_' + str(i), '% of number of objects loaded')
    #make_cdf(amp_size, nonamp_size, './figs/bytes_in_' + str(i), '% of bytes loaded')


amp_dns_linedata = ECDF(amp_dns_lens)
nonamp_dns_linedata = ECDF(nonamp_dns_lens)

plt.figure(figsize=(5.5,5.5))
line1, = plt.plot(amp_dns_linedata.x, amp_dns_linedata.y, lw=3, label='AMP')
line2, = plt.plot(nonamp_dns_linedata.x, nonamp_dns_linedata.y, lw=3, label='Non AMP')

plt.legend(handles=[line1, line2], loc=4)
plt.xlabel('Number of Domain Resolved during Page Load')
plt.ylim(0,1)
plt.ylabel('CDF')
plt.savefig("figs/domain.pdf", bbox_inches="tight")
plt.savefig("figs/domain.png", bbox_inches="tight")
plt.close()

