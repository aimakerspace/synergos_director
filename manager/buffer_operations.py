#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs


# Custom
from .base import BaseOperator

##################
# Configurations #
##################



##########################################
# Buffer operator Class - BufferOperator #
##########################################

class BufferOperator(BaseOperator):
    """ 
    Contains management functionality to buffer queue related oeprations. 
    """
    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key = 'SynMQ_topic_buffer'
        self.queue = 'buffer'
        self.auto_ack = True

        # Connect to channel and exchange
        super().__connect_channel()

        # Network attributes


        # Data attributes
    
        
        # Model attributes


        # Optimisation attributes


        # Export Attributes

    def listen_message(self):
        '''
        Begin message consumption from "buffer" queue on current consumer
        :return:
        '''

        self.__bind_consumer()
        self.channel.basic_consume(queue=self.queue,
                                   on_message_callback=message_callback,
                                   auto_ack=self.auto_ack)

        self.channel.start_consuming()


    ############
    # Checkers #
    ############


    ###########    
    # Helpers #
    ###########
    def __bind_consumer(self):
    '''
    Bind consumer to "buffer" queue
    '''
    self.channel.queue_bind(exchange=self.exchange,
                            queue= self.queue,
                            routing_key=self.routing_key)


def message_callback(ch, method, properties, body):
    '''
    callback function to execute when message received by consumer
    '''
    print(" [x] %r:%r" % (method.routing_key, body))


    ##################
    # Core Functions #
    ##################
