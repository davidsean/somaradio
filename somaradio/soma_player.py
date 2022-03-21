import os
import json
import logging

import vlc
import pika

from somaradio.soma_station import SomaStation


class SomaPlayer:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)

        credentials = pika.PlainCredentials('soma', 'soma')
        parameters = pika.ConnectionParameters(os.environ.get('AMQP_HOST'),
                                       os.environ.get('AMQP_PORT'),
                                       '/',
                                       credentials)
        self._logger.info('connecting with AMQP parameter: %s', parameters)
        self._connection = pika.BlockingConnection(parameters)
        channel = self._connection.channel()
        channel.queue_declare(queue='soma_player')
        channel.basic_consume(queue='soma_player',
                      auto_ack=True,
                      on_message_callback=self.digest_amqp)

        self.vlc_instance = vlc.Instance('--verbose 2'.split())

        # self.vlc_instance = vlc.Instance()

        self.player = self.vlc_instance.media_player_new()
        self.station = None
        self._logger.info("Instantiation successful")

        channel.start_consuming()

    def __del__(self):
        if self.player is not None:
            self.player.stop()
        self._connection.close()


    def digest_amqp(self, ch, method, properties, body: bytes):
        self._logger.info("ch: %s:%s | method: %s:%s | properties: %s:%s | body: %s:%s",
                          ch, type(ch), method, type(method), properties, type(properties), body, type(body))

        payload = json.loads(body.decode('utf-8'))
        self._logger.info("Message payload: %s", payload)
        if 'cmd' in payload:
            if payload['cmd'] == 'stop':
                self.stop()
            elif payload['cmd'] == 'play':
                self.play()
            elif payload['cmd'] == 'set_station':
                try:
                    station = SomaStation(title=payload['station']['title'],
                                        desc=payload['station']['desc'],
                                        playlist_url=payload['station']['playlist_url']
                                        )
                    self.set_station(station)
                except KeyError as exc:
                    self._logger.error(exc)
                self.play()

    def set_station(self, station:SomaStation) -> None:
        self.station = station

    def stop(self):
        self.player.stop()

    def play(self):
        if self.station is not None:
            media = self.vlc_instance.media_new(self.station.tracks[0])
            self.player.set_media(media)
            self.player.play()
        else:
            self._logger.warn("Cannot play without station. Use call play_station first.")
