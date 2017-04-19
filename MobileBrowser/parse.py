from __future__ import division
lines = open('result.txt').readlines()

total = [0 for i in range(5)]

i = 0

while i < len(lines):
    page = int(lines[i].split(':')[1])
    no_links = int(lines[i+1].split(':')[1])
    no_amp = int(lines[i+2].split(':')[1])

    total[page-1] += no_amp / (no_amp + no_links) # relative percentage

    i += 3


print [v / (len(lines) / 15) for v in total]
