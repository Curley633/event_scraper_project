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

print("\n******TICKETMASTER WEB SCRAPER EXECUTING******")
url = 'https://www.ticketmaster.ie/browse/hard-rock-metal-catid-200/music-rid-10001'
oldTablePath = 'C:/Users/James/repos/web_scraper/ticketmaster_events.csv'

while True:

    ticketmaster_events = {}
    event_no = 0
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    ticketmaster_concerts = soup.find_all('li', {'class': 'sc-17c7lsa-1 kMlhUL'})
    print(response)

    for ticketmaster_concert in ticketmaster_concerts:
        artist = ticketmaster_concert.find('span', {'class': 'fuisff-3 bWKPkY'}).text
        # replace commas with dashes for multiple artists to avoid csv errors.
        artist = artist.replace(',', '-')
        location = ticketmaster_concert.find('span', {'class': 'fuisff-4 gWMnZL'}).text
        month = ticketmaster_concert.find('div', {'class': 'sc-1se6fet-1 exbPiQ'}).text
        day = ticketmaster_concert.find('div', {'class': 'sc-1se6fet-2 eeiZWg'}).text
        ticketLink = ticketmaster_concert.find('a').get('href')

        event_no += 1
        ticketmaster_events[event_no] = [artist, location, month, day, ticketLink]
        # print(artist, location, month, day, ticketLink)
    break
print("Total new Events: ", event_no)

try:
    if os.path.exists(oldTablePath):
        os.remove(oldTablePath)
    ticketmaster_events_df = pd.DataFrame.from_dict(ticketmaster_events, orient='index', columns=['name', 'location', 'month', 'day', 'ticketLink'])
    ticketmaster_events_df.head()
    ticketmaster_events_df.to_csv('ticketmaster_events.csv')
except OSError:
    print("ERROR: Can't Write file to this location: ", oldTablePath)
    print("EXITING")
    sys.exit(1)

conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_pword, host=db_host, port='5432', sslmode='require')
cur = conn.cursor()

# Use this for testing connection to postGres
# print(conn.get_dsn_parameters(), "\n")
cur.execute("SELECT version();")
record = cur.fetchone()
print("You are connected to - ", record)

cur.execute("""DROP TABLE IF EXISTS ticketmaster_event_table;
CREATE TABLE ticketmaster_event_table(
index int,
name varchar,
location varchar,
month varchar,
day int,
ticketLink varchar PRIMARY KEY)""")

try:
    with open('ticketmaster_events.csv', encoding="utf8") as f:
        next(f)
        cur.copy_from(f, 'ticketmaster_event_table', sep=',')
        conn.commit()
        print("Created new table in postgres, View Data using PGAdmin or HeidiSQL")
except FileNotFoundError:
    print("CSV File not found")
    print("EXITING")
    sys.exit(1)

