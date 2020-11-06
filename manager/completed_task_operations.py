#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in


# Libs


# Custom
from .base import ConsumerOperator

##################
# Configurations #
##################

#where to instantiate BufferOperator Consumer? How to ensure only one consumer?

##########################################
# Buffer operator Class - BufferOperator #
##########################################

class CompletedTaskOperator(ConsumerOperator):
    """ 
    Contains management functionality to buffer queue related oeprations. 
    """
    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key = 'SynMQ_topic_completed_task'
        self.queue = 'completed_task'
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


if __name__=='__main__':
    completed_task_consume = CompletedTaskOperator()
    completed_task_consume.listen_message()