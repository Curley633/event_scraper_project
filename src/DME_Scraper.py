import sys
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_pword = os.getenv("DB_PWORD")
db_host = os.getenv("DB_HOST")

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

    for concert in concerts:
        title = concert.find('a').text
        details = concert.find('p').text
        link = concert.find('a').get('href')

        event_no += 1
        dme_events[event_no] = [title, details, link]

        # comment back in for testing
        # print('Event\n', title, '\nEvent Page:', link, '\nDetails:', details, '\n---')
    break

try:
    if os.path.exists(oldTablePath):
        os.remove(oldTablePath)
    dme_events_df = pd.DataFrame.from_dict(dme_events, orient='index', columns=['title', 'details', 'link'])
    dme_events_df.head()
    dme_events_df.to_csv('dme_events.csv')
except OSError:
    print("Can't delete file at this location: ..It may be open.", oldTablePath)
    print("EXITING")
    sys.exit(1)
print(event_no)
conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pword, host=db_host, port='5432', sslmode='require')
cur = conn.cursor()

# Comment back in for testing connection to postGreSQL
# print(conn.get_dsn_parameters(), "\n")
cur.execute("SELECT version();")
record = cur.fetchone()
print("You are connected to - ", record)

cur.execute("""DROP TABLE IF EXISTS dme_events_table;
CREATE TABLE dme_events_table(
index int,
title varchar,
details varchar,
link varchar PRIMARY KEY)""")

try:
    with open('dme_events.csv', encoding="utf8", mode='r') as f:
        next(f)
        cur.copy_from(f, 'dme_events_table', sep=',')
        conn.commit()
        print("Created new DME table in postgres, View Data using PGAdmin or HeidiSQL")
except FileNotFoundError:
    print("CSV File not found")
    print("EXITING")
    sys.exit(1)
