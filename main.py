from dotenv import load_dotenv
import os
import pika
import ssl

load_dotenv()

credentials = pika.PlainCredentials(
   os.getenv('RABBITMQ_USER'),
   os.getenv('RABBITMQ_PASS')
)

context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

params = pika.ConnectionParameters(
   host='b-1a6e9d8b-302d-4391-a974-e813635ae438.mq.eu-north-1.amazonaws.com',
   port=5671,
   virtual_host='/',
   credentials=credentials,
   ssl_options=pika.SSLOptions(context)
)

connection = pika.BlockingConnection(params)
channel = connection.channel()

# Publish message
channel.basic_publish(
   exchange='',
   routing_key='queue_name',
   body='test message'
)

connection.close()
# Rest of connection code stays same