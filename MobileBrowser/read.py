import pickle

AMP_SCRIPTS = ['preconnect.gif', 'amp-analytics-0.1.js', 'v0/amp-ad-0.1.js', 'v0.js', 'google/v9.js', 'v0/amp-iframe-0.1.js', 'amp-analytics-0.1.js', 'amp-iframe-0.1.js']

d = pickle.load(open('prefetch_amp_size.pickle', 'rb'))

entries = d[u'log'][u'entries']

text_size = 0
image_size = 0
script_size = 0
other_size = 0

for entry in entries:
    if 'cdn.ampproject.org' in entry[u'request'][u'url']:
        measure = True
        for filename in AMP_SCRIPTS:
            if entry[u'request'][u'url'].endswith(filename):
                measure=False
                break
        if not measure:
            continue
        print entry[u'request'][u'url']
        mimeType = entry[u'response'][u'content'][u'mimeType']
        size = entry[u'response'][u'bodySize']

        if 'javascript' in mimeType:
            script_size += size
        elif 'text/html' in mimeType:
            text_size += size
        elif 'image' in mimeType:
            image_size += size
        else:
            other_size += size

print text_size
print image_size
print script_size
print other_size

