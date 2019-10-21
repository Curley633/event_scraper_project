import sys

from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2
import os

url = 'https://www.ticketmaster.ie/browse/hard-rock-metal-catid-200/music-rid-10001'
oldTablePath = 'C:/Users/James/Documents/venv/npo_ticketmaster_events.csv'

dictionary = {'key': 'value'}
print(dictionary)
dictionary['new key'] = 'new value'
print(dictionary)

while True:

    npo_ticketmaster_events = {}
    event_no = 0
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    ticketmaster_concerts = soup.find_all('li', {'class': 'sc-17c7lsa-1 iMroit'})
    print(response)

    for ticketmaster_concert in ticketmaster_concerts:
        name = ticketmaster_concert.find('span', {'class': 'fuisff-3 gAOxsI'}).text
        location = ticketmaster_concert.find('span', {'class': 'fuisff-4 gpeoHh'}).text
        month = ticketmaster_concert.find('div', {'class': 'sc-1se6fet-1 guQGJM'}).text
        day = ticketmaster_concert.find('div', {'class': 'sc-1se6fet-2 NNWNb'}).text
        ticketLink = ticketmaster_concert.find('a').get('href')

        event_no += 1
        npo_ticketmaster_events[event_no] = [name, location, month, day, ticketLink]
    break
print("Total new Events: ", event_no)

# Comment back in for testing connection to postGreSQL
# print(conn.get_dsn_parameters(), "\n")
# cur.execute("SELECT version();")
# record = cur.fetchone()
# print("You are connected to - ", record, "\n")

try:
    os.remove(oldTablePath)
    npo_ticketmaster_events_df = pd.DataFrame.from_dict(npo_ticketmaster_events, orient='index', columns=['name', 'location', 'month', 'day', 'ticketLink'])
    npo_ticketmaster_events_df.head()
    npo_ticketmaster_events_df.to_csv('npo_ticketmaster_events.csv')

except OSError:
    print("Can't delete file at this location: ", oldTablePath)
    print("EXITING")
    sys.exit(1)
conn = psycopg2.connect(user="user", password="0000", host="localhost", port="5432", dbname="EventScraper")
cur = conn.cursor()

cur.execute("""DROP TABLE IF EXISTS ticketmaster_event_table;
CREATE TABLE ticketmaster_event_table(
index int,
name varchar,
location varchar,
month varchar,
day int,
ticketLink varchar PRIMARY KEY)""")
conn.commit()

try:
    with open('npo_ticketmaster_events.csv', 'r') as f:
        next(f)
        cur.copy_from(f, 'ticketmaster_event_table', sep=',')
        conn.commit()
except FileNotFoundError:
    print("CSV File not found, Line 71")
    print("EXITING")
    sys.exit(1)

