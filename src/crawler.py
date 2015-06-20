__author__ = 'Alan'
# based on common implementation

import re
import urllib2
from bs4 import BeautifulSoup

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def is_valid_url(url):
    if regex.match(url) is not None:
        return True
    return False


def crawler(url):
    to_crawl = [url]
    crawled = set()
    while to_crawl and len(crawled) <= 20:
        page = to_crawl.pop()
        try:
            page_source = urllib2.urlopen(page)
            s = page_source.read()
            soup = BeautifulSoup(s)
            links = soup.findAll('a', href=True)
            if page not in crawled:
                for l in links:
                    if is_valid_url(l['href']):
                        to_crawl.append(l['href'])
                crawled.add(page)
                print 'Crawled:' + page
        except urllib2.URLError, e:
            print(e.message)
            continue
    return crawled


def crawl(url):
    urls = crawler(url)
    f = open('crawled_urls.txt', 'w')
    for ele in urls:
        f.write(ele + '\n')
    f.close()


crawl('http://www.northeastern.edu/careers/')