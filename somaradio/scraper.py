import re
import requests
from bs4 import BeautifulSoup
from typing import List

from app.soma_station import SomaStation

def scrape_stations()->List[SomaStation]:
    """ returns a SomaStation list
    Get a list of radio stations from https://somafm.com/listen
    The SomaStation objects have the station title, description and MP3 stream urls
    
    Returns:
        List[SomaStation]: A list of stations
    """

    source = requests.get('https://somafm.com/listen/').text
    soup = BeautifulSoup(source, 'html5lib')
    stations = soup.find('div', id='stations')
    base_url = 'http://soma.fm'
    playlist_url = None

    for list_item in stations.find_all('li'):
        title = list_item.find('h3').text
        desc = list_item.find('p', class_='descr').text
        station_data_nobr = list_item.find_all('nobr')
        for nobr in station_data_nobr:
            if nobr.find(text=re.compile('MP3 PLS \(SSL\):')):
                u = nobr.find('a', href=True)
                playlist_url = base_url + str(u['href'])
        stations.append(SomaStation(title, desc, playlist_url))

    return stations

if __name__ == '__main__':
    print(scrape_stations())