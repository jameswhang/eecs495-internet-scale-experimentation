import requests
from bs4 import BeautifulSoup

#INPUT_FILE = open('wp_subdirectories.txt').readlines()
#OUTPUT_FILE = open('WPLinks.txt', 'wb')
WP_URL = 'https://www.washingtonpost.com/'

links = []
written_links = []


def search_url(url):
    try:
        wp_home = requests.get(WP_URL, timeout=5)
    except Exception:
        return


    wp_home_s = BeautifulSoup(wp_home.text)

    all_links = wp_home_s.find_all('a')

    for link in all_links:
        try:
            href = link['href']
            if href.startswith('https://www.washingtonpost.com/news/'):
                links.append(href)
        except Exception:
            pass

    for link in links:
        newslink = link.split('https://www.washingtonpost.com/')[1]
        amp_link = 'https://www.washingtonpost.com/amphtml/' + newslink

        try:
            if requests.get(amp_link, timeout=5).status_code == 200:
                if link not in written_links:
                    print link + ',' + amp_link
                    written_links.append(link)
        except Exception:
            pass

if __name__ == '__main__':
    search_url(WP_URL)
    #for url in INPUT_FILE: 
    #    search_url(url.replace('\n', ''))
