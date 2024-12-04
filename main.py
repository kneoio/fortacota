import os

import stomp
from dotenv import load_dotenv

from utils.logger import logger

load_dotenv()

HOST = os.getenv('MQ_HOST')
PORT = int(os.getenv('MQ_PORT', 61614))
QUEUE = os.getenv('MQ_QUEUE')

class MyListener(stomp.ConnectionListener):
   def on_error(self, frame):
       logger.error(f'Error: "{frame.body}"')
   def on_message(self, frame):
       logger.info(f'Message received: "{frame.body}"')

conn = stomp.Connection([(HOST, PORT)])
logger.debug(f'Connecting to {HOST}:{PORT}')

conn.set_listener('', MyListener())
conn.set_ssl(for_hosts=[(HOST, PORT)])
conn.connect(os.getenv('MQ_USER'), os.getenv('MQ_PASS'), wait=True)
logger.info('Connected to ActiveMQ')

conn.subscribe(destination=f'/queue/{QUEUE}', id=1, ack='auto')
logger.debug(f'Subscribed to queue: {QUEUE}')

test_msg = 'test message'
conn.send(body=test_msg, destination=f'/queue/{QUEUE}')
logger.debug(f'Sent message: {test_msg}')

try:
   logger.info('Listening for messages (Ctrl+C to exit)...')
   while True: pass
except KeyboardInterrupt:
   logger.info('Disconnecting...')
   conn.disconnect()