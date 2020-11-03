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
    def create(self, project_id, expt_id, run_id, participant_id):
        """ Creates an operation payload to be sent to a remote queue for 
            linearising jobs for a Synergos cluster
        """
        pass
    
    def delete(self):
        """ Removes an operation payload that had been sent to a remote queue 
            for job linearisation
        """
        pass
    
    def process(self, kwargs):
        # split kwargs into individual messages
        for kwarg in kwargs:
            message = self.create(kwarg)
            self.publish_message(message)

        pass 

    # 

        # also need to do the unstr() of our msg
        # string representation of TinyDate() must be converted back 
        # to the same date format that was from database.json with start_proc 
