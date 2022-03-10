
import re
import vlc
import struct

import urllib.request as urllib2
from typing import List

from app.soma_station import SomaStation
from app.scraper import scrape_stations


class SomaPlayer:

    def __init__(self):
        # scrape soma.fm for stations
        self.stations: List[SomaStation] = scrape_stations()
        self.vlc_instance = vlc.Instance('--verbose 2'.split())
        self.player = self.vlc_instance.media_player_new()
        self.station_index = 0

    def play_station(self, index: int) -> None:
        self.station_index = index
        self.player.stop()
        station = self.stations[index]
        media = self.vlc_instance.media_new(station.tracks[0])
        self.player.set_media(media)
        self.player.play()

    def get_track_description(self) -> str:
        """ get a description of the current track

        Returns:
            str: The description of the current track
        """
        encoding = 'iso-8859-1'
        station = self.stations[self.station_index]
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


