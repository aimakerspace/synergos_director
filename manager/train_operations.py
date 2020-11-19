#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging

# Libs
import pika

# Custom
from .base import ProducerOperator

##################
# Configurations #
##################



#########################################################
# Train producer operator Class - TrainProducerOperator #
#########################################################

class TrainProducerOperator(ProducerOperator):
    """ 
    Contains management functionality to training queue related producer operations.
    """

    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key = 'SynMQ_topic_train'
        
        self.connect_channel()

        logging.debug("Instantiated TrainOperator()")