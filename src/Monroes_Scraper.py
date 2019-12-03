#!/usr/bin/python
import os
import sys
import psycopg2
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://monroes.ie/events/'
oldTablePath = 'C:/Users/James/repos/event_scraper_project/src/monroes_events.csv'

# Create dictionary
dictionary = {'key': 'value'}
print(dictionary)
# Update dictionary
dictionary['new key'] = 'new value'
print(dictionary)

lc_messages = 'en_US'

while True:

    monroes_events = {}
    event_no = 0
    response = requests.get(url)
    data = response.text
    print(response)
    soup = BeautifulSoup(data, 'html.parser')
    monroes_concerts = soup.find_all('div', {'class': 'flexmedia flexmedia--artistevents'})

    for monroes_concert in monroes_concerts:
        artistName = monroes_concert.find('span', {'class': 'artisteventsname'}).text
        # replace commas with dash for multiple artists to avoid csv errors.
        artistName = artistName.replace(',', '-')
        location = 'Monroes - Galway'
        date = monroes_concert.find('span', {'class': 'artisteventstime'}).text
        price = monroes_concert.find('span', {'class': 'artistseventsprice'}).text
        eventLink = monroes_concert.find('a').get("href")

        event_no += 1
        monroes_events[event_no] = [artistName, location, date, price, eventLink]
        # Comment back in for error checking
        # print('Name\n', artistName, '\nLocation\n', location, '\nDate\n', date, '\nPrice\n', price, '\nTickets\n',
        #       eventLink, '\n-----')
    break
print("Total new Events: ", event_no)

try:
    if os.path.exists(oldTablePath):
        os.remove(oldTablePath)
    monroes_events_df = pd.DataFrame.from_dict(monroes_events, orient='index', columns=['Name', 'Location', 'Date', 'Price', 'Event'])
    monroes_events_df.head()
    monroes_events_df.to_csv('monroes_events.csv')
except OSError:
    print("Can't delete file - It may be open")
    sys.exit(1)

conn = psycopg2.connect(dbname='EventScraper', user='postgres', password='curley', host='206.189.165.104', port='5432', sslmode='require')
cur = conn.cursor()

# Use this for testing connection to postGres
print(conn.get_dsn_parameters(), "\n")
cur.execute("SELECT version();")
record = cur.fetchone()
print("You are connected to - ", record, "\n")

cur.execute("""DROP TABLE IF EXISTS monroes_event_table;
CREATE TABLE monroes_event_table(
Index int,
Name varchar,
Location varchar,
Date varchar,
Price varchar,
Event varchar PRIMARY KEY)""")

try:
    with open('monroes_events.csv', encoding="utf8") as f:
        next(f)
        cur.copy_from(f, 'monroes_event_table', sep=',')
        conn.commit()
        print("Created new table in postgres, View Data using PGAdmin or HeidiSQL")
except FileNotFoundError:
    print("CSV File not found")
    print("EXITING")
    sys.exit(1)
