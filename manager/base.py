#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs
import pika

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
    Contains baseline functionality to all queue related oeprations. 
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
        self.exchange = 'SynMQ_topic_logs'
        self.exchange_type = 'topic'
        self.durability = True


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
        self.channel.exchange_declare(exchange=self.exchange,
                                      exchange_type=self.exchange_type,
                                      durable=self.durability)


    ##################
    # Core Functions #
    ##################
    #abstract  methods