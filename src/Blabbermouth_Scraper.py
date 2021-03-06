import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pword = os.getenv("DB_PWORD")
db_host = os.getenv("DB_HOST")

print("\n******BLABBERMOUTH WEB SCRAPER EXECUTING******")
url = 'https://www.blabbermouth.net/news'
oldTablePath = 'C:/Users/James/repos/event_scraper_project/src/blabbermouth_articles.csv'

all_blabbermouth_articles = {}
article_no = 0

while article_no <= 100:
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    blabbermouth_articles = soup.find_all('article', {'class': 'category-news'})

    for blabbermouth_article in blabbermouth_articles:
        # replace commas with dash for multiple artists to avoid csv errors.
        title = blabbermouth_article.find('a').get('title').replace(',', ' - ')
        pre_date = blabbermouth_article.find('span').text.strip()
        date = pre_date.replace(',', ' - ')
        shortLink = blabbermouth_article.find('a').get('href')
        link = "https://www.blabbermouth.net" + shortLink
        # print(title)
        # print(date)
        # print(link)

        article_no += 1
        all_blabbermouth_articles[article_no] = [title, date, link]

    next_page_tag = soup.find('a', {'class': 'next_page'})
    if next_page_tag and next_page_tag.get('href'):
        url = 'https://www.blabbermouth.net' + next_page_tag.get('href')
    else:
        print("END OF LAST PAGE")
        break
print("Total articles: ", article_no)


try:
    if os.path.exists(oldTablePath):
        os.remove(oldTablePath)
    blabbermouth_articles_df = pd.DataFrame.from_dict(all_blabbermouth_articles, orient='index', columns=['title', 'date', 'link'])
    blabbermouth_articles_df.head()
    blabbermouth_articles_df.to_csv('blabbermouth_articles.csv')
except OSError:
    print("Can't delete file at this location: ..It may be open.", oldTablePath)
    print("EXITING")
    sys.exit(1)
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pword, host=db_host, port='5432', sslmode='require')
cur = conn.cursor()

# Comment back in for testing connection to postGreSQL
# print(conn.get_dsn_parameters(), "\n")
cur.execute("SELECT version();")
record = cur.fetchone()
print("You are connected to - ", record)

cur.execute("""DROP TABLE IF EXISTS blabbermouth_news_article_table;
CREATE TABLE blabbermouth_news_article_table(
index int,
title varchar,
date varchar,
link varchar PRIMARY KEY)""")

try:
    with open('blabbermouth_articles.csv', encoding="utf8", mode='r') as f:
        next(f)
        cur.copy_from(f, 'blabbermouth_news_article_table', sep=',')
        conn.commit()
        print("Created new table in postgres, View Data using PGAdmin or HeidiSQL")
except FileNotFoundError:
    print("CSV File not found")
    print("EXITING")
    sys.exit(1)
