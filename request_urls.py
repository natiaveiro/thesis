from googlesearch import search

suspicious_websites = ['svobodnoslovo.eu', 'afera.bg', 'budnaera.com']
current = []

query = "covid site:"  #TODO add other keywords
for url in suspicious_websites:
    current = list(search(query+url, tld="co.in", num=10, stop=10, pause=2))
    print(current)
    with open(url+'.txt', 'w') as f:
        f.write('\n'.join(str(c) for c in current))
