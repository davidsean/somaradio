import pika
import json
import time

AMQP_HOST="localhost"
AMQP_PORT=5672

credentials = pika.PlainCredentials('soma', 'soma')
parameters = pika.ConnectionParameters(AMQP_HOST,
                                AMQP_PORT,
                                '/',
                                credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()
channel.queue_declare(queue='soma_player')


body = {'cmd': 'set_station',
    'station': {
        'title': 'The Trip',
        'desc': 'Progressive house / trance. Tip top tunes.',
        'playlist_url':'https://somafm.com/nossl/thetrip.pls'
    }
}
channel.basic_publish(exchange='', routing_key='soma_player', body=json.dumps(body))


# body = {'cmd': 'play'}
# channel.basic_publish(exchange='', routing_key='soma_player', body=json.dumps(body))

# body = {'cmd': 'stop'}
# channel.basic_publish(exchange='', routing_key='soma_player', body=json.dumps(body))

connection.close()


