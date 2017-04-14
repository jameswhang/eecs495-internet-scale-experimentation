from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

MOBILE_USER_AGENT = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1'



def google_search(driver, keyword):
    driver.get("http://www.google.com")
    elem = driver.find_element_by_class_name("gsfi")
    elem.clear()
    elem.send_keys(keyword)
    elem.send_keys(Keys.RETURN)
    driver.close()

    

def chrome_search(keywords):
    opts = Options()
    opts.add_argument("user-agent={}".format(MOBILE_USER_AGENT))
    driver = webdriver.Chrome(chrome_options=opts)
    google_search(driver, keywords[0])


def firefox_search(keywords):
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", MOBILE_USER_AGENT)
    driver = webdriver.Firefox(profile)
    google_search(driver, keywords[0])


def main():
    keywords = ['China', 'Trump']
    #firefox_search(keywords)
    chrome_search(keywords)
    


if __name__ == '__main__':
    main()
