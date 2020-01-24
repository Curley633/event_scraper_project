import re
import sys
import os
from bs4 import BeautifulSoup
import requests
import pandas as pd
import psycopg2

print("\n******METAL CELL WEB SCRAPER EXECUTING******")
url = 'https://themetalcell.fireside.fm/'
oldTablePath = 'C:/Users/James/repos/event_scraper_project/src/metal_cell_podcasts.csv'
metal_cell_podcasts = {}
podcasts_count = 0

while True:
    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    podcasts = soup.find_all('div', {'class': 'list-item prose'})

    for podcast in podcasts:
        episode_title_temp = podcast.find('a').text
        episode_title = episode_title_temp.replace(',', ' -')
        # print(episode_title)
        episode_page = podcast.find('a').get('href')
        episode_full_url = url + episode_page
        # print(episode_full_url)

        date_temp = podcast.find('i', {'class': 'far fa-calendar-alt'}).findNextSibling(text=True).strip()
        date_temp = re.sub(r'\|', '', date_temp).strip()
        date = date_temp.replace('\"', '')
        date = date_temp.replace(',', ' -')
        re.search(r"^\s+$", date)
        # print(date)
        duration = podcast.find('i', {'class': 'far fa-clock'}).findNextSibling(text=True).strip()
        # print(duration)

        mp3_url = episode_full_url
        response = requests.get(mp3_url)
        data = response.text
        soup = BeautifulSoup(data, 'html.parser')
        podcastMp3 = soup.find(property='og:audio:secure_url').get('content')
        print(podcastMp3)

        podcasts_count += 1
        metal_cell_podcasts[podcasts_count] = [episode_title, date, duration, episode_full_url, podcastMp3]

        # comment back in for testing
        print('Title:\n', episode_title, '\nDate:\n', date, '\nDuration\n', duration, '\nLink to page:\n', episode_full_url,
              '\nMP3:', podcastMp3, '\n-----')

    break

print("Total Podcasts: ", podcasts_count)
# print('Title:\n', episode_title, '\nDate:\n', date, '\nDuration\n', duration, '\nLink to page:\n', episode_full_url, '\nMP3:', podcastMp3, '\n-----')
try:
    if os.path.exists(oldTablePath):
        os.remove(oldTablePath)
    metal_cell_df = pd.DataFrame.from_dict(metal_cell_podcasts, orient='index', columns=['title', 'date', 'duration', 'link', 'mp3'])
    metal_cell_df.head()
    metal_cell_df.to_csv('metal_cell_podcasts.csv')
except OSError:
    print("Can't delete file at this location: ..It may be open.", oldTablePath)
    print("EXITING")
    # sys.exit(1)
conn = psycopg2.connect(dbname='EventScraper', user='postgres', password='curley', host='206.189.165.104', port='5432', sslmode='require')
cur = conn.cursor()

# Comment back in for testing connection to postGreSQL
# print(conn.get_dsn_parameters(), "\n")
cur.execute("SELECT version();")
record = cur.fetchone()
print("You are connected to - ", record)

cur.execute("""DROP TABLE IF EXISTS metal_cell_podcasts;
CREATE TABLE metal_cell_podcasts(
index int,
title varchar,
date varchar,
duration varchar,
link varchar,
mp3 varchar PRIMARY KEY)""")

try:
    with open('metal_cell_podcasts.csv', encoding="utf8", mode='r') as f:
        next(f)
        cur.copy_from(f, 'metal_cell_podcasts', sep=',')
        conn.commit()
        print("Created new Metal Cell Podcasts table in postgres, View Data using PGAdmin or HeidiSQL")
except FileNotFoundError:
    print("CSV File not found")
    print("EXITING")
    sys.exit(1)
