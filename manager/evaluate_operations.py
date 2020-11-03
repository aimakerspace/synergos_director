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



############################################
# Evaluation operator Class - EvaluateOperator #
############################################

class EvaluateOperator(ProducerOperator):
    """ 
    Contains management functionality to buffer queue related operations.
    """
    def __init__(self, host=None):
        # General attributes
        super().__init__(host)
        self.routing_key= 'SynMQ_topic_evaluate'

        # Connect to channel and exchange
        super().__connect_channel()

    # def publish_message(self, message):
    #     '''
    #     Publish single message to "evaluate" queue in exchange
    #     :param message: str
    #     '''
    #     self.channel.basic_publish(exchange=self.exchange_name,
    #                                routing_key=self.routing_key,
    #                                body=message,
    #                                properties=pika.BasicProperties(
    #                                    delivery_mode=2,
    #                                ))

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
    # def process(self, kwargs):
    # # split kwargs into individual messages
    # # an individual message for each run
    #     for run in kwargs['runs']:
    #         run_kwarg = kwargs.copy()
    #         run_kwarg['runs'] = [run]
    #         # string run_kwarg
    #         message = self.create(run_kwarg)
    #         self.publish_message(message)