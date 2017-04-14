from browsermobproxy import Server
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import random
import pprint
import pickle

PICKLE = open('prefetch_amp_size.pickle', 'wb')
MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.1 Mobile/14E5239e Safari/602.1'

server = Server("/Users/jameswhang/Documents/projects/AMP/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

pp = pprint.PrettyPrinter(indent=2)

def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;') 
    return page_state == 'complete'

def is_captcha(driver):
    return 'sorry' in driver.current_url


def google_search(driver, keyword):
    proxy.new_har(keyword)
    driver.get("http://www.google.com")
    elem = driver.find_element_by_class_name("gsfi")
    elem.clear()
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)
    sleep(random.random() * 10 + 5)
    pp.pprint(proxy.har) # returns a HAR JSON blob
    pickle.dump(proxy.har, PICKLE)

def main():
    profile  = webdriver.FirefoxProfile()
    profile.set_proxy(proxy.selenium_proxy())
    profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)
    driver = webdriver.Firefox(firefox_profile=profile)
    keywords = open('./keywords_2.txt').readlines()
    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        google_search(driver, keyword)

    driver.close()


if __name__ == '__main__':
    main()
