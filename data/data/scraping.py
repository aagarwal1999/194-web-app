import requests
from bs4 import BeautifulSoup
import json
from newspaper import Article
import pandas as pd
from urllib.parse import urlparse
# from outfile import run
import csv


# scraping function
# def medicalnews_rss():
#     try:
#         r = requests.get('https://medicalxpress.com/rss')
#         return print('The scraping job succeeded: ', r.status_code)
#     except Exception as e:
#         print('The scraping job failed. See exception: ')
#         print(e)
# print('Starting scraping')
# medicalnews_rss()
# print('Finished scraping')

# def medicalnews_rss():
#     try:
#         r = requests.get('https://medicalxpress.com/rss')
#         soup = BeautifulSoup(r.content, features='xml')
#         return print(soup)
#     except Exception as e:
#         print('The scraping job failed. See exception: ')
#         print(e)

def save_function(article_list):
    with open('medrss.txt', 'w') as outfile:
        json.dump(article_list, outfile)

def save_text(article_list):
    text_data=[]
    for a in article_list:
        article = Article(a['link'])
        article.download()
        article.parse()
        article.nlp()
        text_data.append([a['title'], article.text, urlparse(a['link']).netloc])
    df = pd.DataFrame(text_data, columns = ['Title', 'Text', 'Domain'])
    # filename = 'data_links_data.csv' ## TODO: clean this up
    filename = "".join(args.input.split('.')[:-1]) + '_data.csv'
    df.to_csv(filename)

def test_article(article_text):
    valid =True
    art_tokenized = article_text.tokenize()
    if art_tokenized.text.length <10: 
        valid==False
    elif art_tokenized.text.contains(adwords):
        valid=False
    return valid


def medicalnews_rss(source_links_list):
    article_list = []
    # try:
    for rss_link in source_links_list:
        try:
            # import pdb; pdb.set_trace()
            r = requests.get(rss_link[0])
            soup = BeautifulSoup(r.content, features='xml')
            articles = soup.findAll('item')        
            for a in articles:
                title = a.find('title').text
                link = a.find('link').text
                published = a.find('pubDate').text
                article = {
                    'title': title,
                    'link': link,
                    'published': published
                    }
                article_list.append(article)
        except:
            print('This link is currently not accessible: ', rss_link[0])
    # processedlist = run()
    # save_function(article_list)
        
    return save_text(article_list)
# except Exception as e:
#     print('The scraping job failed. See exception: ')
#     print(e)




if __name__ == "__main__":
    # data = pd.read_csv("list_urls.csv") 
    # links = data[data.columns[1]]
    # source_links_list = links.values.tolist()

    # source_links = ['https://www.medscape.com/cx/rssfeeds/2700.xml', 'https://www.medicaldaily.com/rss', 'https://www.medpagetoday.com/rss/headlines.xml', ]
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default='link_files/data_links.csv')
    args = parser.parse_args()
    # import pdb; pdb.set_trace()
    
    with open(args.input) as f:
        reader = csv.reader(f)
        data = list(reader)

    print(data)
    medicalnews_rss(data)
