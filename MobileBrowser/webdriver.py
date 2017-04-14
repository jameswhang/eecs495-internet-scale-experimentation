from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'


def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;') 
    return page_state == 'complete'

def count_amp(driver):
    while not page_has_loaded(driver):
        sleep(3)
    links = driver.find_elements_by_css_selector("a")
    result_count = 0
    amp_count = 0
    hrefs = []
    for link in links:
        href = link.get_attribute('href')
        if href is None or 'javascript' in href:
            continue
        if link.is_displayed() and not href.startswith('/') and 'google' not in href and href not in hrefs:
            print href
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
    sleep(3)

    pncount = 1  # Pagination Counter

    result_count, amp_count = count_amp(driver)
    print 'Page: ' + str(pncount)
    print 'Number of links: ' + str(result_count)
    print 'Number of amp: ' + str(amp_count)

    while pncount < 5:
        next_btn = driver.find_element_by_id("pnnext")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        ActionChains(driver).move_to_element(next_btn).click(next_btn).perform()
        pncount += 1
        sleep(3)
        result_count, amp_count = count_amp(driver)
        print 'Page: ' + str(pncount)
        print 'Number of links: ' + str(result_count)
        print 'Number of amp: ' + str(amp_count)



def chrome_search(keywords):
    opts = Options()
    opts.add_argument("user-agent={}".format(MOBILE_USER_AGENT))
    driver = webdriver.Chrome(chrome_options=opts)
    google_search(driver, keywords[0])


def firefox_search(keyword):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)
    driver = webdriver.Firefox(profile)
    google_search(driver, keyword)
    driver.close()


def main():
    keywords = open('./keywords.txt').readlines()
    for keyword in keywords:
        keyword = keyword.replace('\n', '')
        firefox_search(keyword)
        #firefox_search(keyword)
    #chrome_search(keywords)


if __name__ == '__main__':
    main()
