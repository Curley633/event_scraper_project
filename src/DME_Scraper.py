import sys
import os
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd
import psycopg2

print("\n******DME WEB SCRAPER EXECUTING******")
url = 'https://dme-promotions.com/events'
oldTablePath = 'C:/Users/James/repos/web_scraper/DME_Scraper.csv'
dme_events = {}
event_no = 0

while True:
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    concerts = soup.find_all('div', {'class': 'description'})
    images = soup.find_all('div', {'class': 'featured-image'})

    for concert in concerts:
        title = concert.find('a').text
        details = concert.find('p').text
        link = concert.find('a').get('href')
        images = soup.find_all('div', {'class': 'featured-image'})
        # for image in images:
        # image = images.find('a').get('style')
        # image = re.sub('background-image:url', '', image)
        # image = re.sub('[(\';)]', '', image)

        event_no += 1
        dme_events[event_no] = [title, details, link, images]

        # comment back in for testing
        print('Event\n', title, '\nEvent Page:', link, '\nDetails:', details, '\nImage:', '\n---')

    break

print("Total new Events: ", event_no)

# try:
#     if os.path.exists(oldTablePath):
#         os.remove(oldTablePath)
#     dme_events_df = pd.DataFrame.from_dict(dme_events, orient='index', columns=['image', 'title', 'link'])
#     dme_events_df.head()
#     dme_events_df.to_csv('dme_events.csv')
# except OSError:
#     print("Can't delete file at this location: ..It may be open.", oldTablePath)
#     print("EXITING")
#     sys.exit(1)
# conn = psycopg2.connect(dbname='EventScraper', user='postgres', password='curley', host='206.189.165.104', port='5432', sslmode='require')
# cur = conn.cursor()
#
# # Comment back in for testing connection to postGreSQL
# # print(conn.get_dsn_parameters(), "\n")
# cur.execute("SELECT version();")
# record = cur.fetchone()
# print("You are connected to - ", record)
#
# cur.execute("""DROP TABLE IF EXISTS dme_events_table;
# CREATE TABLE dme_events_table(
# index int,
# title varchar,
# details varchar,
# image varchar,
# link varchar PRIMARY KEY)""")
#
# try:
#     with open('dme_events.csv', encoding="utf8", mode='r') as f:
#         next(f)
#         cur.copy_from(f, 'dme_events_table', sep=',')
#         conn.commit()
#         print("Created new table in postgres, View Data using PGAdmin or HeidiSQL")
# except FileNotFoundError:
#     print("CSV File not found")
#     print("EXITING")
#     sys.exit(1)
