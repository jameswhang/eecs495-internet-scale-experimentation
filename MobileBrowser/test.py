from browsermobproxy import Server
from selenium import webdriver
import pprint

server = Server("/Users/jameswhang/Documents/projects/AMP/browsermob-proxy-2.1.4/bin/browsermob-proxy")
server.start()
proxy = server.create_proxy()

profile  = webdriver.FirefoxProfile()
profile.set_proxy(proxy.selenium_proxy())
driver = webdriver.Firefox(firefox_profile=profile)

pp = pprint.PrettyPrinter(indent=4)



proxy.new_har("google")
driver.get("http://www.google.co.uk")
pp.pprint(proxy.har) # returns a HAR JSON blob

server.stop()
driver.quit()
