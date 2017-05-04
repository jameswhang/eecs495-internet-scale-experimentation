from browsermobproxy import Server
from selenium import webdriver
import pickle
import os

MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.1 Mobile/14E5239e Safari/602.1'


server = Server("/Users/jameswhang/Documents/projects/AMP/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

os.system('sudo ./dnsflush.sh')

profile = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())
profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)

driver = webdriver.Firefox(firefox_profile=profile)

driver.set_page_load_timeout(15)


proxy.new_har("AMP")
#driver.get("https://www.theguardian.com/us-news/2017/may/04/keystone-xl-pipeline-route-trump-job-claim-myth/")
#pickle.dump(proxy.har, open('washingtonpost.nonamp.pickle', 'wb')) # returns a HAR JSON blob

driver.get("https://amp.theguardian.com/us-news/2017/may/04/keystone-xl-pipeline-route-trump-job-claim-myth/")
pickle.dump(proxy.har, open('washingtonpost.amp.pickle', 'wb')) # returns a HAR JSON blob

proxy.stop()
driver.close()

