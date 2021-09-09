import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import datetime
import os

# title, paragraph, date, link, label
title = paragraph = date = link = label = ''


def svobodnoslovo():
    # svobodnoslovo.eu
    global paragraph, link, date, title, label
    content = soup.find("div", attrs={'class': 'entry-content mh-clearfix'})
    children = content.findChildren('p', recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = soup.select('h1', attrs={'class="entry-title"'})[0].text.strip()
    date = soup.select('span', attrs={'class="entry-meta-date updated"'})[0].text.strip()
    label = '1'


def afera():
    # afera.bg
    try:
        global paragraph, link, date, title, label
        content = soup.find("article", attrs={'class': 'single_post'})
        children = content.findChildren('p', recursive=False)  # avoids non direct descendants
        paragraph = ''
        for child in children:
            paragraph += child.text.strip()
        paragraph = paragraph.replace('\n', ' ')
        link = url
        title = soup.select('h1')[1].text.strip()
        date = content.select('span', attrs={'class="post_data"'})[0].text.strip()
        match = re.search(r'\d{2}.\d{2}.\d{4}', date)  # formatting the date due to other redundant information
        date = match.group()
        label = '1'
    except Exception as e1:
        print('no')


def dnevnik():
    # dnevnik.bg
    global paragraph, link, date, title, label
    everything = soup.find("article", attrs={'class': "general-article-v2 article"})
    content = everything.findChild("div", attrs={'class': 'article-content'})
    children = content.findChildren('p', recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = everything.find('h1', attrs={'itemprop': "name headline"}).text.strip()
    date = everything.find('time', attrs={'itemprop': "datePublished"})['datetime'][:10]  # cutting off the timestamp
    date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%y')  # reformatting the date
    label = '0'


def dw():
    # dw.com/bg
    global paragraph, link, date, title, label
    everythin = soup.find("div", attrs={'id': 'bodyContent'})
    content = everythin.findChild("div", attrs={'class': 'longText'})
    children = content.findChildren('p', recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = everythin.find('h1').text.strip()
    date = everythin.find('ul', attrs={'class': "smallList"}).findChild("li").text.strip()
    match = re.search(r'\d{2}.\d{2}.\d{4}', date)  # formatting the date due to other redundant information
    date = match.group()
    label = '0'


def bnr():
    # bnr.bg
    global paragraph, link, date, title, label
    everythin = soup.find("div", attrs={'class': 'news_title'})
    content = everythin.findChild("span", attrs={'itemprop': 'articleBody'})
    children = content.findChildren('p', recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = everythin.find('h1', attrs={'itemprop': "name"}).text.strip()
    date = everythin.find('span', attrs={'itemprop': "datePublished"}).text.strip()
    match = re.search(r'\d{2}.\d{2}.\d{2}', date)  # formatting the date due to other redundant information
    date = match.group()
    label = '0'


def dariknews():
    # dariknews.bg
    global paragraph, link, date, title, label
    # print(title)
    everythin = soup.find("main", attrs={'class': 'page dk-article'})
    paragraph = everythin.findChild("div", attrs={'class': 'article-text-inner-wrapper io-article-body'}).text.strip()
    # print('do we come here?')
    paragraph = paragraph.replace('\n', '').replace('\r\n','').replace('\r','')
    paragraph = paragraph.replace('"', '')
    # string = "a\nb\rv"
    # paragraph = " ".join(string.splitlines())
    link = url
    title = everythin.find('h1', attrs={'class': "article-title", 'itemprop':'name'}).text.strip()
    date = everythin.find('time', attrs={'class': "time-stamp"})['datetime'][:10]  # cutting off the timestamp
    date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%y')  # reformatting the date
    label = '0'


def news():
    # news.bg
    global paragraph, link, date, title, label
    everything = soup.find("article", attrs={'class': "article-inner"})
    content = everything.findChild("div", attrs={'class': 'article-text'})
    children = content.findChildren('p', recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = everything.find('h1', attrs={'itemprop': "headline"}).text.strip()
    date = everything.find('p', attrs={'itemprop': "datePublished"})['content'][:10]  # cutting off the timestamp
    date = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%d.%m.%y')  # reformatting the date
    label = '0'


def anonybulgaria():
    # anonybulgaria.wordpress.com
    global paragraph, link, date, title, label
    everything = soup.find("div", attrs={'id': "content"})
    content = everything.findChild("div", attrs={'class': 'entry-content'})
    children = content.findChildren({'p', 'ul'}, recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = everything.find('h1', attrs={'class': "entry-title"}).text.strip()
    match = re.search(r'\d{4}/\d{2}/\d{2}', link)  # formatting the date due to other redundant information
    date = match.group()
    date = datetime.datetime.strptime(date, '%Y/%m/%d').strftime('%d.%m.%y')  # reformatting the date
    label = '1'


def thebulgariantimes():
    # thebulgariantimes.com
    global paragraph, link, date, title, label
    everything = soup.find("div", attrs={'class': "theiaStickySidebar"})
    content = everything.findChild("div", attrs={'class': 'entry-content'})
    children = content.findChildren({'h2', 'h3'}, recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = everything.find('h1', attrs={'class': "post-title post-item-title"}).text.strip()
    date = everything.find('time', attrs={'itemprop': "datePublished"}).text.strip()  # cutting off the timestamp
    label = '1'


def anoncyberarmy():
    global paragraph, link, date, title, label
    everything = soup.find("div", attrs={'id': "content"})
    content = everything.findChild("div", attrs={'class': 'entry-content'})
    children = content.findChildren({'p', 'ul'}, recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip()
    paragraph = paragraph.replace('\n', ' ')
    link = url
    title = everything.find('h1', attrs={'class': "entry-title"}).text.strip()
    date = everything.find('time', attrs={'class': "entry-date"}).text.strip()  # cutting off the timestamp
    label = '1'


mapper = {
    'svobodnoslovo': svobodnoslovo,
    'afera': afera,
    'dw': dw,
    'dnevnik': dnevnik,
    'bnr': bnr,
    'dariknews': dariknews,
    'news': news,
    'thebulgariantimes': thebulgariantimes,
    'anonybulgaria': anonybulgaria,
    'anoncyberarmy': anoncyberarmy
}

headers_url = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' \
                             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                             'Chrome/75.0.3770.80 Safari/537.36'}
# this is used to tell the website it's a web browser accessing it

upperframe = []
# text_file = open("dw.txt", "r")
# lines = []
# for line in text_file:
#     lines.append(line.replace('\n', ''))

filename = "NEWS_tbt.csv"
f = open(filename, "w", encoding='utf-8')
headers = "Title,Article,Date,URL,Label"
f.write(headers + '\n')

path = '/Users/nataliazheleva/PycharmProjects/thesis/text_files2/'
text_files = os.listdir(path)

for text_file in text_files:
    file_urls = open(path + text_file, 'r')
    for url in file_urls:
        url = url.strip('\n')
        try:
            page = requests.get(url, headers=headers_url)  # this might throw an exception if something goes wrong.

        except Exception as e:  # this describes what to do if an exception is thrown
            print('ERROR FOR LINK:', url)  # print the link that cause the problem
            continue  # ignore this page. Abandon this and go back.
        time.sleep(2)
        soup = BeautifulSoup(page.text, 'html.parser')
        # print(soup)
        frame = []
        try:
            mapper[text_file]()
        except:
            pass

        if not title:
            # print(url + 'has no title')
            pass
        if not date:
            # print(url + 'has no date')
            pass
        if not paragraph:
            # print(url + 'has no paragraph')
            pass
        if not label:
            # print(url + 'has no label')
            pass
        frame.append((title, paragraph, date, link, label))
        f.write(
            title.replace(',', '^').replace('"', '') + ',' + paragraph.replace(",", "^").replace('"', '') + ',' +
            date + "," + link.replace('\n', '') + ',' + label + '\n')
        upperframe.extend(frame)
f.close()
data = pd.DataFrame(upperframe, columns=['Title', 'Article', 'Date', 'URL', 'Label'])
