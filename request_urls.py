from googlesearch import search
import os
import urllib.request
headers_url = 'Chrome/75.0.3770.80'

websites = ['anoncyberarmy.wordpress.com']

fake_news = ['svobodnoslovo.eu', 'afera.bg',
             'anonybulgaria.wordpress.com', 'thebulgariantimes.com', 'anoncyberarmy.wordpress.com']


current = []

query = "ковид site:"
# query = "ваксина site:"

# os.mkdir('/Users/nataliazheleva/PycharmProjects/thesis/text_files2')


for url in websites:
    current = list(search(query+url, tld="co.in", num=50, stop=50, pause=2, user_agent=headers_url))
    print(current)
    file_name = url.partition('.')[0]
    print(file_name)
    with open(file_name, 'w') as f:
        f.write('\n'.join(str(c) for c in current))
