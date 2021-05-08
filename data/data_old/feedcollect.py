from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd
import feedparser

req = Request("https://www.medicinenet.com/script/main/art.asp?articlekey=24357#rss")
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")
RSS_KEYS= ['rss-feed', '.xml']

links = []
for link in soup.findAll('a'):
    links.append(link.get('href'))

print('#####################ALL LINKS ##########################')
print(links)
    
def valid_rss(link):
    if not link:
        return False
    elif sum([key in link for key in RSS_KEYS])!=0:
        return True
    d = feedparser.parse(link)
    if len(d.entries)==0:
        return False
    return True

rss_links=[]
for link in links: 
    if valid_rss(link): 
        rss_links.append(link)

df = pd.DataFrame(rss_links)
df.to_csv('Rsslinks.csv')

print('#############RSS LINKS#################')
print(rss_links)
# print(is_rss('None'))