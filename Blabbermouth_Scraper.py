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
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    blabbermouth_articles = soup.find_all('article', {'class': 'category-news'})

    for blabbermouth_article in blabbermouth_articles:
        image = blabbermouth_article.find('img').get('src')
        title = blabbermouth_article.find('a').get('title').replace(',', ' - ')
        shortLink = blabbermouth_article.find('a').get('href')
        link = "https://www.blabbermouth.net" + shortLink

        article_no += 1
        all_blabbermouth_articles[article_no] = [image, title, link]

    next_page_tag = soup.find('a', {'class': 'next_page'})
    if next_page_tag and next_page_tag.get('href'):
        url = 'https://www.blabbermouth.net' + next_page_tag.get('href')
    else:
        print("END OF LAST PAGE")
        break
print("Total articles: ", article_no)

try:
    os.remove(oldTablePath)
    blabbermouth_articles_df = pd.DataFrame.from_dict(all_blabbermouth_articles, orient='index',
                                                      columns=['image', 'title', 'link'])
    blabbermouth_articles_df.head()
    blabbermouth_articles_df.to_csv('blabbermouth_articles.csv')
except OSError:
    print("Can't delete file at this location: ", oldTablePath)
    print("EXITING")
    sys.exit(1)
conn = psycopg2.connect(user="user", password="0000", host="localhost", port="5432", dbname="EventScraper")
cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS blabbermouth_news_article_table;
CREATE TABLE blabbermouth_news_article_table(
index int,
image varchar,
title varchar,
link varchar PRIMARY KEY)""")
conn.commit()

try:
    with open('blabbermouth_articles.csv', 'r') as f:
        next(f)
        cur.copy_from(f, 'blabbermouth_news_article_table', sep=',')
        conn.commit()
except FileNotFoundError:
    print("CSV File not found, Line 71")
    print("EXITING")
    sys.exit(1)
