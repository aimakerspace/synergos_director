#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs
import pika

# Custom
from .base import ProducerOperator

##################
# Configurations #
##################



########################################
# Train operator Class - TrainOperator #
########################################

class TrainOperator(ProducerOperator):
    """ 
    Contains management functionality to training queue related operations.
    """

    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key = 'SynMQ_topic_train'

        # Connect to channel and exchange
        super().__connect_channel()

    # def publish_message(self, message):
    #     '''
    #     Publish single message to "train" queue in exchange
    #     :param message: str
    #     '''
    #     self.channel.basic_publish(exchange=self.exchange_name,
    #                                routing_key=self.routing_key,
    #                                body=message,
    #                                properties=pika.BasicProperties(
    #                                    delivery_mode = 2, # make message persistent
    #                                ))


        # Network attributes


        # Data attributes
    
        
        # Model attributes


        # Optimisation attributes


        # Export Attributes

        # Publish message


    ############
    # Checkers #
    ############


    ###########    
    # Helpers #
    ###########


    ##################
    # Core Functions #
    ##################
