#!/usr/bin/env python

"""
Use Selenium to Measure Web Timing

  Performance Timing Events flow

   navigationStart -> redirectStart -> redirectEnd -> fetchStart -> domainLookupStart -> domainLookupEnd 
     -> connectStart -> connectEnd -> requestStart -> responseStart -> responseEnd 
       -> domLoading -> domInteractive -> domContentLoaded -> domComplete -> loadEventStart -> loadEventEnd
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os

SRC = '/Users/jameswhang/Documents/school/eecs495-ise/eecs495-internet-scale-experimentation/sites/measure_2017_02_13.txt'

ATTEMPT_TIMES = 3

def measure(site):
    # First flush DNS Cache
    os.system('sudo /Users/jameswhang/Documents/school/eecs495-ise/eecs495-internet-scale-experimentation/measure/dnsflush.sh')

    # Fake User Agent as mobile Safari
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>")
    driver = webdriver.Chrome(chrome_options=opts)
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
    print 'link,non_amp_total,non_amp_response,amp_total,amp_response,attempt#'

    sites = open(SRC).readlines()
    for site in sites:
        site = site.replace('\n', '')

        non_amp = site.split(',')[0]
        amp = site.split(',')[1].replace('\n', '')

        for i in range(ATTEMPT_TIMES):
            amp_totaltime, amp_responsetime = measure(amp)
            non_amp_totaltime, non_amp_responsetime = measure(non_amp)
            print site + ',' + non_amp_totaltime + ',' + non_amp_responsetime + ',' + amp_totaltime + ',' + amp_responsetime + ',' + str(i)
            sleep(5)  # sleep 5 sec and try again

