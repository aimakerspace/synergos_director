from .core.exchange_connection import ConnectExchange

class ReceiveTrain(ConnectExchange):
    def __init__(self, host):
        super().__init__(host)
        super().connect_channel()
        self.result = self.channel.queue_declare('train', durable=True)
        self.queue_name = self.result.method.queue
        self.channel.queue_bind(exchange='SynMQ_topic_logs',
                                queue=self.queue_name,
                                routing_key='SynMQ_topic_train')

    def __callback(self, ch, method, properties, body):
        print(" [x] %r:%r" % (method.routing_key, body))

    def receive(self):
        print(' [*] Waiting for logs. To exit press CTRL+C')
        self.channel.basic_consume(queue=self.queue_name,
                                   on_message_callback=self.__callback,
                                   auto_ack=True)

        self.channel.start_consuming()