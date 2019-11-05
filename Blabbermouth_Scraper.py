import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2
import os

url = 'https://www.blabbermouth.net/news'
oldTablePath = 'C:/Users/James/repos/web_scraper/blabbermouth_articles.csv'

dictionary = {'key': 'value'}
print(dictionary)
dictionary['new key'] = 'new value'
print(dictionary)

all_blabbermouth_articles = {}
article_no = 0

while True:
    all_blabbermouth_articles = {}
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    blabbermouth_articles = soup.find_all('article', {'class': 'category-news'})
    print(response)

    for blabbermouth_article in blabbermouth_articles:
        image = blabbermouth_article.find('img').get('src')
        title = blabbermouth_article.find('a').get('title')
        shortLink = blabbermouth_article.find('a').get('href')
        link = "https://www.blabbermouth.net" + shortLink

        # article_no += 1
        all_blabbermouth_articles = [image, title, link]

        next_page_tag = soup.find('a', {'class': 'next_page'})
    if next_page_tag and next_page_tag.get('href'):
        url = 'https://www.blabbermouth.net' + next_page_tag.get('href')
    else:
        print("END OF LAST PAGE")
        break
blabbermouth_articles_df = pd.DataFrame.from_dict(all_blabbermouth_articles, orient='index',
                                                  columns=['image', 'title', 'link'])
blabbermouth_articles_df.head()
blabbermouth_articles_df.to_csv('blabbermouth_articles.csv')
