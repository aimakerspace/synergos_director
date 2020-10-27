from .core.exchange_connection import ConnectExchange

class PublishTrain(ConnectExchange):
    def __init__(self, host):
        super().__init__(host)
        super().connect_channel()

    def publish(self, message, routing_key='SynMQ_topic_train'):
        self.channel.basic_publish(exchange='SynMQ_topic_logs',
                                   routing_key=routing_key,
                                   body=message)