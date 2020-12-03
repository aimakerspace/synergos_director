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

class PreprocessProducerOperator(ProducerOperator):
    """ 
    Contains management functionality to evaluate queue related producer operations.
    """
    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key= 'SynMQ_topic_preprocess'

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
    def process(self, project_id):
        """
        Sends message for project_id to poll involved participants
        """

        preprocess_kwarg = {'project_id' : project_id}
        message = self.create(preprocess_kwarg)
        self.publish_message(message)
        self.connection.close()

        return preprocess_kwarg
