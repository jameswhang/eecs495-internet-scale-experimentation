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
from datetime import date
import os

SRC = './measure_2017_03_13.txt'

ATTEMPT_TIMES = 1

def measure(site):
    # First flush DNS Cache
    os.system('sudo ./dnsflush_ubuntu.sh')

    # Fake User Agent as mobile Safari
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>")
    driver = webdriver.Chrome(chrome_options=opts)
    driver.get(site)
    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")    
    eventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

    requestStart = driver.execute_script("return window.performance.timing.requestStart")
    responseStart = driver.execute_script("return window.performance.timing.responseStart")

    chromeTotalTime = eventEnd - navigationStart
    chromeResponseTime = responseStart - requestStart
    driver.quit()

    # Firefox Measurement
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    firefox_profile.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>")
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.get(site)

    navigationStart = driver.execute_script("return window.performance.timing.navigationStart")    
    eventEnd = driver.execute_script("return window.performance.timing.loadEventEnd")

    requestStart = driver.execute_script("return window.performance.timing.requestStart")
    requestStart = driver.execute_script("return window.performance.timing.requestStart")
    responseEnd = driver.execute_script("return window.performance.timing.responseEnd")

    firefoxTotalTime = eventEnd - navigationStart
    firefoxResponseTime = responseStart - requestStart
    driver.quit()

    return {
        'Chrome': [str(chromeTotalTime), str(chromeResponseTime)],
        'Firefox': [str(firefoxTotalTime), str(firefoxResponseTime)],
    }


if __name__ == '__main__':
    todaystr = str(date.today()).replace('-', '_')

    chrome_output = open('./measurement_chrome_{today}'.format(today=todaystr), 'wb')
    firefox_output = open('./measurement_firefox_{today}'.format(today=todaystr), 'wb')

    chrome_output.write('link,non_amp_total,non_amp_response,amp_total,amp_response,attempt#\n')
    firefox_output.write('link,non_amp_total,non_amp_response,amp_total,amp_response,attempt#\n')

    sites = open(SRC).readlines()
    for site in sites:
        site = site.replace('\n', '')

        non_amp = site.split(',')[0]
        amp = site.split(',')[1].replace('\n', '')
 
        measure(amp)
        measure(non_amp)

        for i in range(ATTEMPT_TIMES):
            try:
                amp_res = measure(amp)
            except Exception:
                amp_res = None
                # Might be a timeout exception, so will sleep a little
                sleep(5)
            try:
                namp_res = measure(non_amp)
            except Exception:
                namp_res = None 

            if amp_res is not None and namp_res is not None:
                chrome_res = amp + ',' + non_amp + ',' + namp_res['Chrome'][0] + ',' + namp_res['Chrome'][1] + ',' + amp_res['Chrome'][0] + ',' + amp_res['Chrome'][1] + ',' + str(i) + '\n'
                firefox_res = amp + ',' + non_amp + ',' + namp_res['Firefox'][0] + ',' + namp_res['Firefox'][1] + ',' + amp_res['Firefox'][0] + ',' + amp_res['Firefox'][1] + ',' + str(i) + '\n'

                print chrome_res
                print firefox_res

                #chrome_output.write(chrome_res)
                #firefox_output.write(firefox_res)

            sleep(5)  # sleep 5 sec and try again

