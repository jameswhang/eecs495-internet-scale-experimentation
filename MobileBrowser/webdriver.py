from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep
import random

resultfile = open('result_9.txt', 'wb')

MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.1 Mobile/14E5239e Safari/602.1'


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;') 
    return page_state == 'complete'

def is_captcha(driver):
    return 'sorry' in driver.current_url

def count_amp(driver):
    if is_captcha(driver):
        print 'CAPTCHA!!!'
        r = raw_input()

    while not page_has_loaded(driver):
        sleep(3)
    links = driver.find_elements_by_css_selector("a")
    result_coun = 0
    amp_count = 0
    hrefs = []
    for link in links:
        href = link.get_attribute('href')
        if href is None or 'javascript' in href:
            continue
        if link.is_displayed() and not href.startswith('/') and 'google' not in href and href not in hrefs:
            hrefs.append(href)
    elem = driver.find_elements_by_class_name("_Ogn")
    for link in elem:
        if 'AMP' in link.text:
            amp_count += 1
    return len(hrefs), amp_count


def google_search(driver, keyword):
    driver.get("http://www.google.com")
    elem = driver.find_element_by_class_name("gsfi")
    elem.clear()
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)
    sleep(random.random() * 10 + 5)

    pncount = 1  # Pagination Counter

    result_count, amp_count = count_amp(driver)
    resultfile.write('Page: ' + str(pncount)+'\n')
    resultfile.write('Number of links: ' + str(result_count)+'\n')
    resultfile.write('Number of amp: ' + str(amp_count)+'\n')

    sleep(random.random() * 10 + 5)

    while pncount < 5:
        if is_captcha(driver):
            print 'CAPTCHA!!!'
            r = raw_input()
        next_btn = driver.find_element_by_id("pnnext")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ActionChains(driver).move_to_element(next_btn).click(next_btn).perform()
        pncount += 1
        sleep(random.random() * 10 + 5)
        result_count, amp_count = count_amp(driver)
        resultfile.write('Page: ' + str(pncount)+'\n')
        resultfile.write('Number of links: ' + str(result_count)+'\n')
        resultfile.write('Number of amp: ' + str(amp_count)+'\n')



def chrome_search(driver, keyword):
    google_search(driver, keyword)


def firefox_search(keyword):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)
    driver = webdriver.Firefox(profile)
    google_search(driver, keyword)
    driver.close()


def main():
    opts = Options()
    opts.add_argument("user-agent={}".format(MOBILE_USER_AGENT))
    driver = webdriver.Chrome(chrome_options=opts)

    keywords = open('./keywords.txt').readlines()
    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        chrome_search(driver, keyword)
    driver.close()


if __name__ == '__main__':
    main()
