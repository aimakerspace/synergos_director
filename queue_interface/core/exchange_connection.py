import pika

class ConnectExchange:
    def __init__(self, host):
        self.host = host
        self.channel = None
        self.connection = None

    def connect_channel(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host= self.host))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='SynMQ_topic_logs',
                                      exchange_type='topic',
                                      durable=True)