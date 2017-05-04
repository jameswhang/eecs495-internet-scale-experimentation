from browsermobproxy import Server
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import pickle
import os

MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.1 Mobile/14E5239e Safari/602.1'

urlsfile = open('urls.txt').readlines()

amp_urls = []
nonamp_urls = []

for line in urlsfile:
    line = line.replace('\n', '')
    amp_urls.append(line.split(',')[1])
    nonamp_urls.append(line.split(',')[0])

assert len(amp_urls) == len(nonamp_urls)

server = Server("/Users/jameswhang/Documents/projects/AMP/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

for i in range(len(amp_urls)):
    os.system('sudo ./dnsflush.sh')

    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.set_page_load_timeout(15)
    proxy.new_har("AMP")
    try:
        driver.get(amp_urls[i])
        amp_har = proxy.har
        
    except TimeoutException as ex:
        driver.quit()
        continue
    driver.quit()

    os.system('sudo ./dnsflush.sh')

    profile = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)

    driver = webdriver.Firefox(firefox_profile=profile)
    driver.set_page_load_timeout(15)
    proxy.new_har("NONAMP")
    try:
        driver.get(nonamp_urls[i])
        nonamp_har = proxy.har
    except TimeoutException as ex:
        driver.quit()
        continue
    
    driver.quit()
    pickle.dump(amp_har, open('./amp_pickles/' + str(i) + '.pickle', 'wb')) # returns a HAR JSON blob
    pickle.dump(nonamp_har, open('./nonamp_pickles/' + str(i) + '.pickle', 'wb')) # returns a HAR JSON blob

    