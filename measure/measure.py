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

TIMING = 'return window.performance.timing.{prop}'
TIMING_PROPERTIES = [
    'navigationStart',
    'unloadEventStart',
    'unloadEventEnd',
    'redirectStart',
    'redirectEnd',
    'fetchStart',
    'domainLookupStart',
    'domainLookupEnd',
    'connectStart',
    'connectEnd',
    'secureConnectionStart',
    'requestStart',
    'responseStart',
    'responseEnd',
    'domLoading',
    'domInteractive',
    'domContentLoadedEventStart',
    'domComplete',
    'loadEventStart',
    'loadEventEnd'
]

ATTEMPT_TIMES = 1

def measure(site):
    # First flush DNS Cache
    os.system('sudo ./dnsflush.sh')

    # Fake User Agent as mobile Safari
    opts = Options()
    opts.add_argument("user-agent=Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>")
    driver = webdriver.Chrome(chrome_options=opts)
    driver.get(site)

    chrome_measurements = []


    for prop in TIMING_PROPERTIES:
        print TIMING.format(prop=prop)
        res = driver.execute_script(TIMING.format(prop=prop))
        chrome_measurements.append(res)

    driver.quit()

    # Firefox Measurement
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("browser.privatebrowsing.autostart", True)
    firefox_profile.set_preference("general.useragent.override", "Mozilla/5.0 (Linux; <Android Version>; <Build Tag etc.>) AppleWebKit/<WebKit Rev> (KHTML, like Gecko) Chrome/<Chrome Rev> Mobile Safari/<WebKit Rev>")
    driver = webdriver.Firefox(firefox_profile=firefox_profile)
    driver.get(site)

    firefox_measurements = []

    for prop in TIMING_PROPERTIES:
        res = driver.execute_script(TIMING.format(prop=prop))
        firefox_measurements.append(res)

        #firefox_measurements.append(driver.execute_script(TIMING.format(prop=prop)))

    driver.quit()

    return {
        'Chrome': chrome_measurements,
        'Firefox': firefox_measurements
    }


def write_header(filehandle):
    filehandle.write('link,')
    filehandle.write(str(TIMING_PROPERTIES).strip('[]').replace('\'', ''))
    filehandle.write('\n')

if __name__ == '__main__':
    todaystr = str(date.today()).replace('-', '_')

    chrome_output_amp = open('./measurement_chrome_amp_{today}'.format(today=todaystr), 'wb')
    chrome_output_non_amp = open('./measurement_chrome_non_amp{today}'.format(today=todaystr), 'wb')
    firefox_output_amp = open('./measurement_firefox_amp{today}'.format(today=todaystr), 'wb')
    firefox_output_non_amp = open('./measurement_firefox_non_amp{today}'.format(today=todaystr), 'wb')

    write_header(chrome_output_amp)
    write_header(chrome_output_non_amp)
    write_header(firefox_output_amp)
    write_header(firefox_output_non_amp)

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
                chrome_res_amp = amp_res['Chrome']
                firefox_res_amp = amp_res['Firefox']
                chrome_res_nonamp = namp_res['Chrome']
                firefox_res_nonamp= namp_res['Firefox']

                for idx, prop in enumerate(chrome_res_amp):
                    chrome_output_amp.write(str(prop))
                    if idx == len(chrome_res_amp) - 1:
                        chrome_output_amp.write('\n')
                    else:
                        chrome_output_amp.write(',')

                for idx, prop in enumerate(firefox_res_amp):
                    firefox_output_amp.write(str(prop))
                    if idx == len(firefox_res_amp) - 1:
                        firefox_output_amp.write('\n')
                    else:
                        firefox_output_amp.write(',')

                for idx, prop in enumerate(chrome_res_nonamp):
                    chrome_output_non_amp.write(str(prop))
                    if idx == len(chrome_res_nonamp) - 1:
                        chrome_output_non_amp.write('\n')
                    else:
                        chrome_output_non_amp.write(',')

                for idx, prop in enumerate(firefox_res_nonamp):
                    firefox_output_non_amp.write(str(prop))
                    if idx == len(firefox_res_nonamp) - 1:
                        firefox_output_non_amp.write('\n')
                    else:
                        firefox_output_non_amp.write(',')

            sleep(5)  # sleep 5 sec and try again

