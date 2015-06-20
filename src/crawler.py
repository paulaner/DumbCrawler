__author__ = 'Alan'
# based on common implementation

import re
import sys
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


def crawler_bfs(url, nums):
    to_crawl = [url]
    crawled = set()
    n = int(nums) - 1
    while to_crawl and len(crawled) <= n:
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


# ### DFS implementation ####
unvisited = []
visited = set()


def crawler_dfs(url, nums):
    if len(unvisited) > 0 and len(visited) <= int(nums) - 1:
        try:
            page_content = urllib2.urlopen(url)
            source = page_content.read()
            parsed_soup = BeautifulSoup(source)
            anchors = parsed_soup.findAll('a', href=True)
            if url not in visited:
                for link in anchors:
                    if is_valid_url(link['href']):
                        unvisited.append(link['href'])
                visited.add(url)
                print 'Crawled:' + url
        except urllib2.URLError, err:
            print(err.message)
            crawler_dfs(unvisited.pop(), nums)
        crawler_dfs(unvisited.pop(), nums)


def crawl(url, nums, visit_type):
    if is_valid_url(url) is False:
        return -1
    if visit_type == "bfs":
        ret = crawler_bfs(url, nums)
    else:
        unvisited.append(url)
        crawler_dfs(url, nums)
        ret = visited
    f = open('crawled_urls.txt', 'w')
    for ele in ret:
        f.write(ele + '\n')
    f.close()


if __name__ == "__main__":
    seed = sys.argv[1]
    limit = sys.argv[2]
    traverse_type = sys.argv[3]
    crawl(seed, limit, traverse_type)
