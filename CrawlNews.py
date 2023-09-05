# Import libraries
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup as bs
import re
import csv
import string
import datetime
import time


def get_next_pages(base_url, url):
    html = urllib.request.urlopen(url)
    soup = bs(html, 'html.parser')
    if not soup.find('a', class_='btn-page next-page'):
        return ''
    next_page = soup.find('a', class_='btn-page next-page').get('href')
    url = base_url + next_page
    return url


def get_next_pages_dantri(base_url, url):
    html = urllib.request.urlopen(url)
    soup = bs(html, 'html.parser')
    if not soup.find('div', class_='pagination').find('a', class_='page-item next'):
        return ''
    next_page = soup.find('div', class_='pagination').find('a', class_='page-item next').get('href')
    return base_url + next_page


def crawl_news(duration=0):
    # VnExpress
    base_url = 'https://vnexpress.net'
    child_url = ['https://vnexpress.net/khoa-hoc', 'https://vnexpress.net/giai-tri', 'https://vnexpress.net/the-thao',
                 'https://vnexpress.net/giao-duc', 'https://vnexpress.net/suc-khoe', 'https://vnexpress.net/du-lich']
    date_crawl = datetime.date.today()
    time_duration = datetime.timedelta(days=duration)
    time_limit = date_crawl - time_duration
    print('--------------------------------------------------------------')
    print('Crawling VnExpress...')
    print('--------------------------------------------------------------')
    titles = []
    links = []
    contents = []
    for url in child_url:
        page_count = 0
        news_count = 0
        exceed_timelim = False
        while not exceed_timelim and page_count < 10:
            if url == '':
                break
            html = urllib.request.urlopen(url)
            soup = bs(html, 'html.parser')
            news = soup.find_all(re.compile('^h[1-9]{1}'), class_=re.compile('title.{1}news'))

            for new in news:
                if new.find('a') and new.find('a').get('title') != None and new.find('a').get('href') != None:
                    title = new.find('a').get('title')
                    link = new.find('a').get('href')
                    if not link.startswith('https'):
                        continue
                    if link in links: continue
                    try:
                        html = urllib.request.urlopen(link)
                    except urllib.error.URLError:
                        print('Fail for link', link)
                        continue
                    soup = bs(html, 'html.parser')
                    description = soup.find('p', class_='description')
                    if description != None:
                        if description.span != None: description.span.extract()
                        content = description.text + ' '
                    body = soup.find_all('p', class_='Normal')
                    for para in body:
                        if para == body[-1] and len(para.text.split()) < 10: break
                        if para.text not in content: content = content + re.sub('\s+', ' ', para.text) + ' '
                    if len(content.split()) < 10: continue
                    if not soup.find('span', class_='date') or soup.find('span', class_='date').text == '':
                        continue
                    date = soup.find('span', class_='date').text.split(',')[1].strip()
                    day, month, year = [int(x) for x in date.split('/')]
                    if datetime.date(year, month, day) < time_limit:
                        exceed_timelim = True
                        break

                    titles.append(title)
                    links.append(link)
                    contents.append(content.strip())
                    news_count += 1
                    time.sleep(1)
            url = get_next_pages(base_url, url)
            page_count += 1

    # Dan tri
    print('------------------------------------------')
    print('Crawling DanTri...')
    print('------------------------------------------')
    base_url = 'https://dantri.com.vn'
    child_url = ['https://dantri.com.vn/the-thao.htm', 'https://dantri.com.vn/giai-tri.htm',
                 'https://dantri.com.vn/giao-duc-huong-nghiep.htm', 'https://dantri.com.vn/suc-khoe.htm',
                 'https://dantri.com.vn/du-lich.htm']
    for url in child_url:
        page_count = 0
        news_count = 0
        exceed_timelim = False
        while not exceed_timelim and page_count < 10:
            if url == '':
                break
            html = urllib.request.urlopen(url)
            soup = bs(html, 'html.parser')
            news = soup.find_all(re.compile('^h[1-9]{1}'), class_='article-title')

            for new in news:
                if new.find('a').text != None and new.find('a').get('href') != None:
                    title = new.find('a').text
                    link = base_url + new.find('a').get('href')
                    if not link.startswith('https'):
                        continue
                    if link in links: continue
                    try:
                        html = urllib.request.urlopen(link)
                    except urllib.error.URLError:
                        print('Fail for link', link)
                        continue
                    soup = bs(html, 'html.parser')
                    if not soup.find('time') or soup.find('time').get('datetime') == '':
                        continue
                    year, month, day = [int(x) for x in soup.find('time').get('datetime').split()[0].split('-')]
                    if datetime.date(year, month, day) < time_limit:
                        exceed_timelim = True
                        break
                    for s in soup.select('figcaption'):
                        s.extract()
                    body = soup.find_all('p')
                    content = ''
                    for para in body:
                        content = content + para.text
                    content = re.sub('\s+', ' ', content)
                    if len(content.split()) < 10: continue

                    titles.append(title)
                    links.append(link)
                    contents.append(content.strip())
                    news_count += 1
                    time.sleep(1)
            url = get_next_pages_dantri(base_url, url)
            page_count += 1
    print('Total news get:', len(links))
    return (titles, links, contents)


