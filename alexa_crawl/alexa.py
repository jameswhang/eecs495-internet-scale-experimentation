import requests
from bs4 import BeautifulSoup

if __name__ == '__main__':
    alexa_sites = []
    for i in range(1, 20):
        html = requests.get('http://www.alexa.com/topsites/global;{num}'.format(num=i)).text
        soup = BeautifulSoup(html)
        links = soup.find_all('p', attrs={'class': 'desc-paragraph'})
        for link in links:
            a = link.find('a')
            # alexa_sites.append(a['href'].replace('/siteinfo/', ''))
            print a['href'].replace('/siteinfo/', '')


