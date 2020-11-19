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



#################################################################
# Evaluation producer operator Class - EvaluateProducerOperator #
#################################################################

class EvaluateProducerOperator(ProducerOperator):
    """ 
    Contains management functionality to evaluate queue related producer operations.
    """
    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key= 'SynMQ_topic_evaluate'

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