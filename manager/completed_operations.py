#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs
import argparse

# Custom
from .base import ConsumerOperator

##################
# Configurations #
##################

#where to instantiate Completed Operator Consumer? How to ensure only one consumer?

#################################################################
# Completed consumer operator Class - CompletedConsumerOperator #
#################################################################

class CompletedConsumerOperator(ConsumerOperator):
    """ 
    Contains management functionality to completed queue related consumer operations. 
    """
    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key = 'SynMQ_topic_completed'
        self.queue = 'completed'
        self.auto_ack = True

        # Connect to channel and exchange
        super().connect_channel()

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


def str2none(v):
    '''
    Converts string None to NoneType for module compatibility
    in main.py
    '''
    if v == "None":
        return None
    else:
        return v


if __name__=='__main__':

    parser = argparse.ArgumentParser()

    # receive arguments for synergos mq server host
    parser.add_argument(
        '--host',
        dest='host',
        help='Synergos_MQ server host',
        default=None
    )
    
    args = parser.parse_args()

    completed_consume = CompletedConsumerOperator(host=str2none(args.host))
    completed_consume.listen_message()