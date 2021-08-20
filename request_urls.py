from googlesearch import search
import os

websites = ['svobodnoslovo.eu', 'afera.bg', 'dnevnik.bg', 'dw.com/bg', 'bnr.bg/post', 'dariknews.bg',
                       'news.bg',
                       'anonybulgaria.wordpress.com', 'thebulgariantimes.com', 'anoncyberarmy.wordpress.com']
current = []

query = "ковид site:"

os.mkdir('/Users/nataliazheleva/PycharmProjects/thesis/text_files')


for url in websites:
    current = list(search(query+url, tld="co.in", num=5, stop=5, pause=2))
    print(current)
    file_name = url.partition('.')[0]
    print(file_name)
    with open(file_name, 'w') as f:
        f.write('\n'.join(str(c) for c in current))
