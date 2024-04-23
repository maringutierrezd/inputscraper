import requests
import time
import csv
from threading import Thread

# Global variables
DAY_SECONDS = 24 * 60 * 60
MES_SECONDS = DAY_SECONDS * 30
BASIC_HEADERS = {
        'Accept': '*/*'
    }

# Functions
def update_events_thread(events, eventslist):
    threads = []
    for ev in eventslist:
        threads.append(Thread(target=update_events, args=(events, ev,)))
    
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

def update_events(events, ev):
    # The event detail URL is constructed as follows
    id = ev['id']
    detail_url = f'https://events.xceed.me/v1/events/{id}'
    # The lineup URL (for the artists) is constructed as follows
    lineup_url = f'https://events.xceed.me/v1/events/{id}/line-up'
    event_response = requests.get(detail_url, headers=BASIC_HEADERS)
    lineup_response = requests.get(lineup_url, headers=BASIC_HEADERS)
    event_data = event_response.json()['data']
    lineup_data = lineup_response.json()['data']

    # This comprobation is redundant
    if event_data['id'] in events:
        return None
    new_event = {}
    new_event['name'] = event_data['name']
    new_event['date'] = event_data['startingTime']
    # new_event['about'] = event_data['about']
    new_event['club'] = event_data['venue']['name']

    genres = ''
    # Genres of the event
    for g in event_data['musicGenres']:
        genre_name = g['name']
        if genre_name not in genres:
            genres += ';' + genre_name

    artists = ''
    # Genres of the artists (which do not always define the event's genres)
    for artist in lineup_data:
        artists += ';' + artist['name']
        for g in artist['musicGenres']:
            genre_name = g['name']
            if genre_name not in genres:
                genres += ';' + genre_name

    new_event['artists'] = artists
    new_event['xceed_genres'] = genres
    events[event_data['id']] = new_event

def get_xceed():
    time_now = time.time()

    # Main URL from which all clubs in BCN which use XCEED get the data for their events. URL works as a sort of dictionary for the events, further details must be looked up individually
    events_url = f'https://events.xceed.me/v1/cities/barcelona/events/categories/all-events/events?limit={10**6}?endTime={time_now + MES_SECONDS}'
    response = requests.get(events_url, headers=BASIC_HEADERS)
    
    # The content is returned in JSON format
    content = response.json()['data']

    events = {}
    eventslist = []
    for ev in content:
        eventslist.append(ev)
    
    update_events_thread(events, eventslist)

    # TODO: esto es temporal, eliminar esto y hacerlo bien
    # df = pd.DataFrame(data=events, index=[0])
    # df = (df.T)
    # df.to_excel('resultados.xlsx')
    with open('output.csv', 'w') as output:
        writer = csv.writer(output)
        for key, value in events.items():
            print(value)
            writer.writerow([key, value])

# Main function
def main():
    t1 = time.time()
    get_xceed()
    print(time.time() - t1)

if __name__ == '__main__':
    main()
