from datetime import date
import requests
from bs4 import BeautifulSoup

HOME_URL = 'http://time.com/'

links = []
written_links = []

def isInt(s):
   try: 
       int(s)
       return True
   except ValueError:
       return False

def search_url(url):
    try:
        wp_home = requests.get(url, timeout=5)
    except Exception:
        print 'Exception in request!!'
        return

    wp_home_s = BeautifulSoup(wp_home.text)

    all_links = wp_home_s.find_all('a')
    today_str = str(date.today()).replace('-', '/')

    for link in all_links:
        try:
            href = link['href']
            if href.startswith('http://time.com') and isInt(href.split('/')[3]):
                links.append(href)
        except Exception:
            pass

    for link in links:
        link = link[:-13]
        amp_link = link.replace('http://time.com/', 'http://amp.timeinc.net/time/')
        try:
            if requests.get(amp_link, timeout=5).status_code == 200:
                if link not in written_links:
                    print link + ',' + amp_link
                    written_links.append(link)
        except Exception:
            pass

if __name__ == '__main__':
    search_url(HOME_URL)
    #for url in INPUT_FILE: 
    #    search_url(url.replace('\n', ''))
