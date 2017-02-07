#!/usr/bin/env python

"""
Use Selenium to Measure Web Timing

  Performance Timing Events flow

   navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd 
     -> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd 
       -> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd
"""

from selenium import webdriver


SRC = 'wp_sites.txt'

def measure(site):
    driver = webdriver.Chrome()
    driver.get(site)
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")    
    eventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

    requestStart = driver.execute_script("return window.performance.timing.requestStart")
    responseEnd = driver.execute_script("return window.performance.timing.responseEnd")

    totalTime = eventEnd - navigationStart
    responseTime = responseEnd - requestStart

    driver.quit()

    return str(totalTime), str(responseTime)


if __name__ == '__main__':
    print 'link,non_amp_total,non_amp_response,amp_total,amp_response'

    sites = open(SRC).readlines()
    for site in sites:
        site = site.replace('\n', '')

        non_amp = site.split(',')[0]
        amp = site.split(',')[1].replace('\n', '')

        non_amp_totaltime, non_amp_responsetime = measure(non_amp)
        amp_totaltime, amp_responsetime = measure(amp)

        print site + ',' + non_amp_totaltime + ',' + non_amp_responsetime + ',' + amp_totaltime + ',' + amp_responsetime + ''
