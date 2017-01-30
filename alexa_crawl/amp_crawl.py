import requests
from bs4 import BeautifulSoup

AMP_SCRIPT = "https://cdn.ampproject.org/v0.js"
ALEXA_SITES = open('alexa500.txt').readlines()
ALEXA_AMP_ANALYTICS = open('alexa500_amp_nalyzed.txt', 'wb')
URL_FORMAT = 'http://www.{url}'

def fetch_html(site):
    try:
        html = requests.get(URL_FORMAT.format(url=site)).text
    except requests.exceptions.ConnectionError:
        print 'CONNECTION ERROR WHILE ACCESSING: ' + site + ', ABORTING...'
        html = ''
    except requests.exceptions.TooManyRedirects:
        print 'REDIRECTION ERROR WHILE ACCESSING: ' + site + ', ABORTING...'
        html = ''
    except requests.exceptions.InvalidURL:
        print 'Invalid URL. Aborting...'
        html = ''
    except Exception:
        print 'Unknown exception. Aborting...'
        html = ''
    return html

def check_is_amp(html):
    return AMP_SCRIPT in html

def write_to_result(site, is_amp, amp_site=None):
    if is_amp:
        print site + ' is an AMP site!!'
        ALEXA_AMP_ANALYTICS.write(site+'\t'+'True\t' + amp_site + '\n')
    else:
        print site + ' is not an AMP site!!'
        ALEXA_AMP_ANALYTICS.write(site+'\t'+'False\n')

for site in ALEXA_SITES:
    site = site.replace('\n', '')
    html = fetch_html(site)
    is_amp = check_is_amp(html)

    if is_amp:
        write_to_result(site, True, amp_site=site)
        continue
    
    soup = BeautifulSoup(html)
    links = soup.find_all('a')

    links_for_this_site = []
    for link in links:
        if 'href' not in link:
            continue
        if link['href'] not in links_for_this_site:
            links_for_this_site.append(link['href'])

    for link in links_for_this_site:
        html = fetch_html(link)
        if check_is_amp(html):
            write_to_result(site, True, amp_site=link)
            break
