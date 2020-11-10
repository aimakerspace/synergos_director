#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging

# Libs
import pika
import json

# Custom
from .abstract import AbstractOperator

##################
# Configurations #
##################

# reduce log level
logging.getLogger("pika").setLevel(logging.WARNING)


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

        # Optimisation attributes
        # e.g multiprocess/asyncio if necessary for optimisation

        # Export Attributes 
        # e.g. any artifacts that are going to be exported eg Records

    
        


    ############
    # Checkers #
    ############


    ###########    
    # Helpers #
    ###########
    def connect_channel(self):
        '''
        Initiate connection with RabbitMQ exchange where queues exist
        '''
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=self.exchange_name,
                                      exchange_type=self.exchange_type,
                                      durable=self.durability)
        # Turn on delivery confirmations
        self.channel.confirm_delivery()


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
        try:
            self.channel.basic_publish(exchange=self.exchange_name,
                                    routing_key=self.routing_key,
                                    body=message,
                                    properties=pika.BasicProperties(
                                        delivery_mode=2,
                                        ))
            logging.info('Message publish was confirmed')
        except pika.exceptions.UnroutableError:
            logging.info('Message could not be confirmed')

    def process(self, kwargs):
        """
        Splits kwargs into individual messages, one message for each run
        Returns number of messages published with publish_message()

        """
        published_count = 0
        for experiment in kwargs['experiments']:
            
            curr_expt_id = experiment['key']['expt_id']
            
            for run in kwargs['runs']:
                
                if run['key']['expt_id'] == curr_expt_id:
                    run_kwarg = kwargs.copy()

                    # redacted code for previously incompatible start_proc kwarg
                    # run_kwarg.update({
                    #     'keys' : run['key'],
                    #     'experiment': experiment,
                    #     'run' : run
                    # })
                    run_kwarg['experiments'] = [experiment]
                    run_kwarg['runs'] = [run]

                    # redacted code for previously incompatible start_proc kwarg
                    # run_kwarg.pop('experiments')
                    # run_kwarg.pop('runs')

                    message = self.create(run_kwarg)
                    self.publish_message(message)
                    published_count = published_count + 1

        self.connection.close()

        return published_count

class ConsumerOperator(BaseOperator):
    """
    Management functionality for message consumers
    """
    def __init__(self, host=None):
        super().__init__(host)
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
        print (f"Listening from {self.queue} queue: ")
        self.channel.start_consuming()

    def message_callback(self, ch, method, properties, body):
        '''
        callback function to execute when message received by consumer
        '''
        print(" [x] %r:%r" % (method.routing_key, body))