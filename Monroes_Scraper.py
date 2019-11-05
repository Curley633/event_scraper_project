import os
import sys
import psycopg2
from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://monroes.ie/events/'
oldTablePath = 'C:/Users/James/repos/web_scraper/npo_monroes_events.csv'

# Create dictionary
dictionary = {'key': 'value'}
print(dictionary)
# Update dictionary
dictionary['new key'] = 'new value'
print(dictionary)

lc_messages = 'en_US'

while True:

    npo_monroes_events = {}
    event_no = 0
    response = requests.get(url)
    data = response.text
    print(response)
    soup = BeautifulSoup(data, 'html.parser')
    monroes_concerts = soup.find_all('div', {'class': 'flexmedia flexmedia--artistevents'})

    for monroes_concert in monroes_concerts:
        artistName = monroes_concert.find('span', {'class': 'artisteventsname'}).text
        location = 'Monroes - Galway'
        date = monroes_concert.find('span', {'class': 'artisteventstime'}).text
        price = monroes_concert.find('span', {'class': 'artistseventsprice'}).text
        ticketLink = monroes_concert.find('a').get("href")

        event_no += 1
        npo_monroes_events[event_no] = [artistName, location, date, price, ticketLink]
        # Comment back in for error checking
        # print('Name\n', artistName, '\nLocation\n', location, '\nDate\n', date, '\nPrice\n', price, '\nTickets\n',
        #       ticketLink, '\n-----')
    break
print("Total new Events: ", event_no)

try:
    os.remove(oldTablePath)
    npo_monroes_events_df = pd.DataFrame.from_dict(npo_monroes_events, orient='index', columns=['Name', 'Location', 'Date', 'Price', 'Tickets'])
    npo_monroes_events_df.head()
    npo_monroes_events_df.to_csv('npo_monroes_events.csv')
except OSError:
    print("Can't delete file as it does not exist")
    sys.exit(1)

conn = psycopg2.connect(user="user", password="0000", host="localhost", port="5432", dbname="EventScraper")
cur = conn.cursor()

# Comment back in for testing connection to postGreSQL
# print(conn.get_dsn_parameters(), "\n")
# cur.execute("SELECT version();")
# record = cur.fetchone()
# print("You are connected to - ", record, "\n")

cur.execute("""DROP TABLE IF EXISTS monroes_event_table;
CREATE TABLE monroes_event_table(
Index int,
Name varchar,
Location varchar,
Date varchar,
Price varchar,
Tickets varchar PRIMARY KEY)""")

try:
    with open('npo_monroes_events.csv', encoding="utf8") as f:
        next(f)
        cur.copy_from(f, 'monroes_event_table', sep=',')
        conn.commit()
except FileNotFoundError:
    print("CSV File not found, Line 71")
    print("EXITING")
    sys.exit(1)
