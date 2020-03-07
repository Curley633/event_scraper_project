import re
import sys
from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2
import os

print("\n******OVERDRIVE WEB SCRAPER EXECUTING******")
url = 'https://www.overdrive.ie/category/news/'
oldTablePath = 'C:/Users/James/repos/event_scraper_project/src/overdrive_articles.csv'

all_overdrive_articles = {}
article_no = 0

while True:
    response = requests.get(url)
    print(response)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    overdrive_articles = soup.find_all('div', {'class': 'large-8 columns page'})

    for overdrive_article in overdrive_articles:
        print(overdrive_articles)

        # replace commas with dash for multiple artists to avoid csv errors.
        # title = overdrive_article.find('a').text
        # pre_date = overdrive_article.find('span').text.strip()
        # date = pre_date.replace(',', ' - ')
        # shortLink = overdrive_article.find('div').get('post-thumb-holder large-6 columns').
        # link = overdrive_article.find('a').get('href')
        # print(title)
        # print(date)
        # print(link)

        article_no += 1
        # print(article_no)
        # all_overdrive_articles[article_no] = [title, date, link]
    break

#     next_page_tag = soup.find('a', {'class': 'next_page'})
#     if next_page_tag and next_page_tag.get('href'):
#         url = 'https://www.blabbermouth.net' + next_page_tag.get('href')
#     else:
#         print("END OF LAST PAGE")
#         break
# print("Total articles: ", article_no)
