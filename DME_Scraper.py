from bs4 import BeautifulSoup
import requests
import pandas as pd


url = 'https://dme-promotions.com/events'

# dictionary = {'key': 'value'}
# print(dictionary)
# dictionary['new key'] = 'new value'
# print(dictionary)

while True:

    npo_events = {}
    event_no = 0

    response = requests.get(url)
    data = response.text
    soup = BeautifulSoup(data, 'html.parser')
    concerts = soup.find_all('div', {'class': ['event odd', 'event even']})
    # concerts = soup.find_all("a", string="+")
    print(response)

    for concert in concerts:
        name = concert.find('a').get('href')
        date = concert.findAll('a')[1]
        print(date.text.strip(), '=>', date.attrs['href'])
        print(soup.text)
        # venue = concert.find()
        # eventLink = concert.find('a').get('href')
        # ticketLink = concert.find('a', {'class': 'tickets'}).get('href')
        # ticketLink = ticketLink.replace(' ', '%20')

        event_no += 1
        # npo_events[event_no] = [eventTitle, eventLink, ticketLink]
        print(name)
        print(date)

        # print('Event\n', eventTitle, '\nEvent Page:', eventLink, '\nTickets:', ticketLink, '\n---')

    break

print("Total new Events: ", event_no)
# npo_events_df = pd.DataFrame.from_dict(npo_events, orient='index', columns=['Event', 'Event Page', 'Tickets'])
# npo_events_df.to_csv('npo_events.csv')
