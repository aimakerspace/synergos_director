#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs
import pika
import json

# Custom
from .abstract import AbstractOperator

##################
# Configurations #
##################



######################################
# Base Operator Class - BaseOperator #
######################################

class BaseOperator(AbstractOperator):
    """ 
    Contains baseline functionality to all queue related operations. 
    """
    def __init__(self, host=None):
        # General attributes
        if not host:
            self.host='localhost'
        else:
            self.host = host

        # Network attributes
        self.channel = None
        self.connection = None
        self.exchange_name = 'SynMQ_topic_logs'
        self.exchange_type = 'topic'
        self.durability = True
        self.routing_key = None


        # Data attributes
        # e.g participant_id/run_id in specific format
            
        # Model attributes
        # (-.-)

        # Optimisation attributes
        # e.g multiprocess/asyncio

        # Export Attributes 

    
        


    ############
    # Checkers #
    ############


    ###########    
    # Helpers #
    ###########
    def __connect_channel(self):
        '''
        Initiate connection with RabbitMQ exchange where queues exist
        '''
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type=self.exchange_type,
                                      durable=self.durability)


    ##################
    # Core Functions #
    ##################
    def create(self, run_kwarg):
        """ Creates an operation payload to be sent to a remote queue for 
            linearising jobs for a Synergos cluster
        """
        return json.dumps(run_kwarg, default=str, sort_keys=True)
        
    
    def delete(self):
        """ 
            Removes an operation payload that had been sent to a remote queue 
            for job linearisation
        """
        pass

    
    def process_consumer(self, message):
        '''
        Convert string message to dictionary
        '''
        return json.loads(message)

        # also need to do the unstr() of our msg
        # string representation of TinyDate() must be converted back 
        # to the same date format that was from database.json with start_proc 

class ProducerOperator(BaseOperator):
    def __init__(self, host=None):
        super().__init__(host)
    
    def publish_message(self, message):
        '''
        Publish single message to "evaluate" queue in exchange
        :param message: str
        '''
        self.channel.basic_publish(exchange=self.exchange_name,
                                   routing_key=self.routing_key,
                                   body=message,
                                   properties=pika.BasicProperties(
                                       delivery_mode=2,
                                   ))
    def process(self, kwargs):
        # split kwargs into individual messages
        # an individual message for each run
        for run in kwargs['runs']:
            run_kwarg = kwargs.copy()
            run_kwarg['runs'] = [run]
            # string run_kwarg
            message = self.create(run_kwarg)
            self.publish_message(message)

class ConsumerOperator(BaseOperator):
    """
    Management functionality for message consumers
    """
    def __init__(self):
        self.queue = None
        self.auto_ack = None

    def __bind_consumer(self):
        '''
        Bind consumer to queue
        '''
        self.channel.queue_bind(exchange=self.exchange_name,
                                queue= self.queue,
                                routing_key=self.routing_key)
    
    def listen_message(self):
        '''
        Begin message consumption from queue on current consumer
        '''
        self.__bind_consumer()
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=self.message_callback,
                                   auto_ack=self.auto_ack)

        self.channel.start_consuming()

    def message_callback(ch, method, properties, body):
        '''
        callback function to execute when message received by consumer
        '''
        print(" [x] %r:%r" % (method.routing_key, body))