import re
import requests

class SomaStation:
    # use this regex pattern to get File*=<URL-TO-SCRAPE!>
    REGEX = r"File\d+=([a-zA-Z0-9/.:-]+)"

    def __init__(self, title:str, desc:str, playlist_url:str) -> None:
        self.title = title
        self.desc = desc
        self.playlist_url = playlist_url
        self.tracks = []
        self._init_tracks()

    def _init_tracks(self):
        """ init track list by fetching url playlist
        This fetches the station playlist and savs the MP3 stream of it's tracks
        """
        resp = requests.get(self.playlist_url)
        resp.raise_for_status()
        # print(resp.text)
        self.tracks = []
        matches = re.findall(SomaStation.REGEX, resp.text)
        for match in matches:
            self.tracks.append(match)
