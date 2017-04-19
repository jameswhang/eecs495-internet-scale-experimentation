from __future__ import division

import glob
import pickle
import matplotlib.pyplot as plt
import matplotlib
import numpy
import statsmodels
from statsmodels.distributions.empirical_distribution import ECDF

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

    text_size = 0
    image_size = 0
    script_size = 0
    other_size = 0
    total_size = 0

    for entry in entries:
        if 'cdn.ampproject.org' in entry[u'request'][u'url']:
            measure = True
            for filename in AMP_SCRIPTS:
                if entry[u'request'][u'url'].endswith(filename):
                    measure=False
                    break
                elif 'preconnect.gif?' in entry[u'request'][u'url']:
                    measure=False
                    break
            if not measure:
                continue
            #print entry[u'request'][u'url']
            mimeType = entry[u'response'][u'content'][u'mimeType']
            size = entry[u'response'][u'bodySize']

            total_size += size

            if 'javascript' in mimeType:
                script_size += size
            elif 'text/html' in mimeType:
                text_size += size
            elif 'image' in mimeType:
                image_size += size
            else:
                other_size += size

    text_sizes.append(text_size)
    image_sizes.append(image_size)
    script_sizes.append(script_size)
    other_sizes.append(other_size)
    total_sizes.append(total_size/1000)


pickles = glob.glob('./pickles/*.pickle')

for picklefile in pickles:
    read_pickle(picklefile)



avg_text = sum(text_sizes) / len(text_sizes)
avg_image = sum(image_sizes) / len(image_sizes)
avg_script = sum(script_sizes) / len(script_sizes)
avg_other = sum(other_sizes) / len(other_sizes)

print 'Average text size: ' + str(sum(text_sizes) / len(text_sizes))
print 'Average image size: ' + str(sum(image_sizes) / len(image_sizes))
print 'Average script size: ' + str(sum(script_sizes) / len(script_sizes))
print 'Average other size: ' + str(sum(other_sizes) / len(other_sizes))
print 'AVERAGE IMPACT: ' + str(avg_text + avg_image + avg_script + avg_other)

make_cdf(total_sizes, 'Average size of prefetched AMP data on Mobile Browser', 'Total Size')
