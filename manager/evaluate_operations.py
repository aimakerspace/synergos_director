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



############################################
# Evaluation operator Class - EvalOperator #
############################################

class EvalOperator(BaseOperator):
    """ 
    Contains management functionality to buffer queue related operations.
    """
    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key= 'SynMQ_topic_evaluate'

        # Connect to channel and exchange
        super().connect_channel()

    def publish_message(self, message):
        '''
        Publish single message to "evaluate" queue in exchange
        :param message: str
        '''
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key=routing_key,
                                   message=message)


        # Network attributes


        # Data attributes
    
        
        # Model attributes


        # Optimisation attributes


        # Export Attributes


    ############
    # Checkers #
    ############


    ###########    
    # Helpers #
    ###########


    ##################
    # Core Functions #
    ##################
