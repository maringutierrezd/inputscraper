import requests
import time

# Global variables
DAY_SECONDS = 24 * 60 * 60
MES_SECONDS = DAY_SECONDS * 30

# Functions
def get_input():
    time_now = time.time() - DAY_SECONDS

    # Main URL from which the input website gets the data for its events. URL works as a sort of dictionary for the events, further details must be looked up individually
    events_url = f'https://events.xceed.me/v1/events?channel=input&startTime={time_now}&endingTime={time_now + 3*MES_SECONDS}&limit=200&orderBy=date&sort=ASC'
    headers =  {
        'Accept': '*/*'
    }
    response = requests.get(events_url, headers=headers)
    
    # The content is returned in JSON format
    content = (response.json())['data']

    artists = []
    # For each element in the output file, get its details from XCEED, individually
    for elem in content:
        # The detail URL is constructed as follows
        detail_url = f'https://events.xceed.me/v1/events/{elem['id']}'
        headers =  {
        'Accept': '*/*'
        }
        response = requests.get(detail_url, headers=headers)
        print(response)

# Main function
def main():
    get_input()

if __name__ == '__main__':
    main()
