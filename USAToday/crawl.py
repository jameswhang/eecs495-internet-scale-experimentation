import requests
from bs4 import BeautifulSoup

HOME_URL = 'http://www.usatoday.com/'

links = []
written_links = []

def search_url(url):
    try:
        wp_home = requests.get(url, timeout=5)
    except Exception:
        print 'Exception in request!!'
        return

    wp_home_s = BeautifulSoup(wp_home.text)

    all_links = wp_home_s.find_all('a')

    for link in all_links:
        try:
            href = link['href']
            if href.startswith('/story/') and '2017' in href:
                links.append(href)
        except Exception:
            pass

    for link in links:
        newsnum = link.split('/')[-2]
        link = 'http://www.usatoday.com/' + link
        amp_link = 'http://amp.usatoday.com/story/{}/'.format(newsnum)
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
