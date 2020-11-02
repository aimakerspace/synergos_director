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



########################################
# Train operator Class - TrainOperator #
########################################

class TrainOperator(BaseOperator):
    """ 
    Contains management functionality to training queue related operations.
    """

    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key = 'SynMQ_topic_train'

        # Connect to channel and exchange
        super().__connect_channel()

    def publish_message(self, message):
        '''
        Publish single message to "train" queue in exchange
        :param message: str
        '''
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=self.routing_key,
                                   body=message)


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
