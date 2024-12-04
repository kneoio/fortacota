# publisher.py
from dotenv import load_dotenv
import os
import stomp
from utils.logger import logger

load_dotenv()

HOST = os.getenv('MQ_HOST')
PORT = int(os.getenv('MQ_PORT', 61614))
QUEUE = os.getenv('MQ_QUEUE')

conn = stomp.Connection([(HOST, PORT)])
logger.debug(f'Connecting to {HOST}:{PORT}')

conn.set_ssl(for_hosts=[(HOST, PORT)])
conn.connect(os.getenv('MQ_USER'), os.getenv('MQ_PASS'), wait=True)
logger.info('Connected to ActiveMQ')

test_msg = 'test message'
conn.send(body=test_msg, destination=f'/queue/{QUEUE}')
logger.debug(f'Sent message: {test_msg}')

conn.disconnect()
logger.info('Disconnected')