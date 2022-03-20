import os
import logging
import vlc
import pika

from somaradio.soma_station import SomaStation


class SomaPlayer:

    def __init__(self):
        self._logger = logging.getLogger(__name__)

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
                      on_message_callback=self.callback)

        self.vlc_instance = vlc.Instance('--verbose 2'.split())
        self.player = self.vlc_instance.media_player_new()
        self.station = None
        self._logger.info("Instantiation successful")

        channel.start_consuming()

    def __del__(self):
        self.player.stop()
        self._connection.close()

    def callback(self, ch, method, properties, body):
        print(" [x] Received %r" % body)

    def set_station(self, station:SomaStation) -> None:
        self.station = station

    def play_station(self, station:SomaStation) -> None:
        self.player.stop()
        self.station = station
        media = self.vlc_instance.media_new(self.station.tracks[0])
        self.player.set_media(media)
        self.player.play()

    def stop(self):
        self.player.stop()

    def play(self):
        if self.station is not None:
            self.player.play()
        else:
            self._logger.warn("Cannot play without station. Use call play_station first.")
