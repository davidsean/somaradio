import re
import requests
import logging
import struct
from bs4 import BeautifulSoup
from typing import List

from somaradio.soma_station import SomaStation


class SomaService:

    def __init__(self):
        self._logger = logging.getLogger(__name__)

        # scrape soma.fm for stations
        self.stations: List[SomaStation] = self.scrape_stations()
        self.station_index = 0
        self._logger.info("Instantiation successful")


    def scrape_stations(self)->List[SomaStation]:
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
                if nobr.find(text=re.compile(r'MP3 PLS \(SSL\):')):
                    u = nobr.find('a', href=True)
                    playlist_url = base_url + str(u['href'])
            stations.append(SomaStation(title, desc, playlist_url))

        return stations

    def get_track_description(self, station:SomaStation) -> str:
        """ get a description of the current track

        Returns:
            str: The description of the current track
        """
        encoding = 'iso-8859-1'
        request = urllib2.Request(station.tracks[0], headers={'Icy-MetaData': 1})
        response = urllib2.urlopen(request)

        metaint = int(response.headers['icy-metaint'])
        for _ in range(10): # # title may be empty initially, try several times
            response.read(metaint)  # skip to metadata
            metadata_length = struct.unpack('B', response.read(1))[0] * 16  # length byte
            metadata = response.read(metadata_length).rstrip(b'\0')

            m = re.search(br"StreamTitle='([^']*)';", metadata)
            if m:
                title = m.group(1)
                if title:
                    break
        return title.decode(encoding, errors='replace')


if __name__ == '__main__':
    print(scrape_stations())