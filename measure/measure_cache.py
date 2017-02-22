#!/usr/bin/env python

"""
Selenium script for measuring cache behavior of AMP CDN
"""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import os

AMP_URL = 'https://www.theguardian.com/us-news/2017/feb/21/donald-trump-immigration-deportation-guidelines-homeland-security,https://amp.theguardian.com/us-news/2017/feb/21/donald-trump-immigration-deportation-guidelines-homeland-security'

ATTEMPT_TIMES = 100

def measure(site):
    # flushing local DNS
    os.system('sudo ./dnsflush.sh')

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
    print 'link,total,response,time slept'

    for i in range(ATTEMPT_TIMES):
        amp_totaltime, amp_responsetime = measure(AMP_URL)
        print AMP_URL + ',' + amp_totaltime + ',' + amp_responsetime + ',' + str(pow(2, i))
        sleep(pow(2, i))  # sleep 2^i seconds and try again

