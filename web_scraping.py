import urllib.request, sys, time
from bs4 import BeautifulSoup
import requests
import pandas as pd

pagesToGet = 1
headers_url = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' \
                             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
                             'Chrome/75.0.3770.80 Safari/537.36'}
# this is used to tell the website it's a web browser accessing it

upperframe = []
text_file = open("fakes.txt", "r")
lines = []
for line in text_file:
    lines.append(line.replace('\n', ''))

filename = "NEWS.csv"
f = open(filename, "w", encoding='utf-8')
headers = "Title,Article,Date,URL,Label"
f.write(headers)
for url in lines:
    try:
        page = requests.get(url, headers=headers_url)  # this might throw an exception if something goes wrong.

    except Exception as e:  # this describes what to do if an exception is thrown
        error_type, error_obj, error_info = sys.exc_info()  # get the exception information
        print('ERROR FOR LINK:', url)  # print the link that cause the problem
        print(error_type, 'Line:', error_info.tb_lineno)  # print error info and line that threw the exception
        continue  # ignore this page. Abandon this and go back.
    time.sleep(2)
    soup = BeautifulSoup(page.text, 'html.parser')
    frame = []

    content = soup.find("div", attrs={'class': 'entry-content mh-clearfix'})
    children = content.findChildren('p', recursive=False)  # avoids non direct descendants
    paragraph = ''
    for child in children:
        paragraph += child.text.strip('\n')
    link = url
    title = soup.select('h1', attrs={'class="entry-title"'})[0].text.strip()
    date = soup.select('span', attrs={'class="entry-meta-date updated"'})[0].text.strip()
    label = '1'
    frame.append((title, paragraph, date, link, label))
    f.write(title.replace(',', '^') + ',' + paragraph.replace(",", "^") + ',' + date + "," + link + ',' + label+'\n')
    upperframe.extend(frame)
f.close()
data = pd.DataFrame(upperframe, columns=['Title', 'Article', 'Date', 'URL', 'Label'])
data.head()
