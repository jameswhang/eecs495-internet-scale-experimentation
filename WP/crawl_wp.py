import requests
from bs4 import BeautifulSoup

OUTPUT_FILE = open('WPLinks.txt', 'wb')
WP_URL = 'https://www.washingtonpost.com/'

wp_home = requests.get(WP_URL)
wp_home_s = BeautifulSoup(wp_home.text)

all_links = wp_home_s.find_all('a')

links = []

written_links = []


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

    if requests.get(amp_link).status_code == 200:
        if link not in written_links:
            print '{},{}'.format(link, amp_link)
            written_links.append(link)
