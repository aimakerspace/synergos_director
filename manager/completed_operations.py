#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import re
import logging

# Libs
import argparse

# Custom
from rest_rpc import app
from .base import ConsumerOperator
from rest_rpc.training.core.hypertuners.tune_driver_script import start_hp_validations

##################
# Configurations #
##################

logging.basicConfig(level=logging.INFO)

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
<<<<<<< HEAD
    def message_callback(self, ch, method, properties, body):
        '''
        callback function to execute when message received by consumer
        '''

        # For hyperparam tuning validations
        if re.search(r"TRAINING COMPLETE .+/optim_run_.*", body.decode()):
            message_components = re.findall(r"[\w\-]+", body.decode())
            project_id = message_components[3]
            expt_id = message_components[4]
            run_id = message_components[5]

            # init_params = request.json

            # Retrieves expt-run supersets (i.e. before filtering for relevancy)
            retrieved_project = project_records.read(project_id=project_id)
            project_action = retrieved_project['action']
            experiments = retrieved_project['relations']['Experiment']
            runs = retrieved_project['relations']['Run']

            # If specific experiment was declared, collapse training space
            if expt_id:

                retrieved_expt = expt_records.read(
                    project_id=project_id, 
                    expt_id=expt_id
                )
                runs = retrieved_expt.pop('relations')['Run']
                experiments = [retrieved_expt]

                # If specific run was declared, further collapse training space
                if run_id:

                    retrieved_run = run_records.read(
                        project_id=project_id, 
                        expt_id=expt_id,
                        run_id=run_id
                    )
                    retrieved_run.pop('relations')
                    runs = [retrieved_run]

            # Retrieve all participants' metadata
            registrations = registration_records.read_all(
                filter={'project_id': project_id}
            )

            # Include all relevant participants
            participants = [record['participant']['id'] 
            for record in registrations]

            kwargs = {
                'action': project_action,
                'experiments': experiments,
                'runs': runs,
                'registrations': registrations,
                'participants': participants,
                'metas': ['evaluate'],
                'version': None # defaults to final state of federated grid
            }

            # kwargs.update(init_params)

            # PRODUCE TRAINING MESSAGE
            if app.config['IS_CLUSTER_MODE']:
                evaluate_operator = EvaluateProducerOperator(host=app.config["SYN_MQ_HOST"])
                result = evaluate_operator.process(project_id, kwargs)

                data = {"run_ids": result}

        print(" [x] %r:%r" % (method.routing_key, body))
        # logging.info(" [x] %r:%r" % (method.routing_key, body))
=======
    # def message_callback(self, ch, method, properties, body):
    #     '''
    #     callback function to execute when message received by consumer
    #     '''

    #     # For hyperparam tuning validations
    #     if re.search(r"TRAINING COMPLETE .+/optim_run_.*", body.decode()):
    #         message_components = re.findall(r"[\w\-]+", body.decode())
    #         project_id = message_components[3]
    #         expt_id = message_components[4]
    #         run_id = message_components[5]

    #         # init_params = request.json

    #         # Retrieves expt-run supersets (i.e. before filtering for relevancy)
    #         retrieved_project = project_records.read(project_id=project_id)
    #         project_action = retrieved_project['action']
    #         experiments = retrieved_project['relations']['Experiment']
    #         runs = retrieved_project['relations']['Run']

    #         # If specific experiment was declared, collapse training space
    #         if expt_id:

    #             retrieved_expt = expt_records.read(
    #                 project_id=project_id, 
    #                 expt_id=expt_id
    #             )
    #             runs = retrieved_expt.pop('relations')['Run']
    #             experiments = [retrieved_expt]

    #             # If specific run was declared, further collapse training space
    #             if run_id:

    #                 retrieved_run = run_records.read(
    #                     project_id=project_id, 
    #                     expt_id=expt_id,
    #                     run_id=run_id
    #                 )
    #                 retrieved_run.pop('relations')
    #                 runs = [retrieved_run]

    #         # Retrieve all participants' metadata
    #         registrations = registration_records.read_all(
    #             filter={'project_id': project_id}
    #         )

    #         # Include all relevant participants
    #         participants = [record['participant']['id'] 
    #         for record in registrations]

    #         kwargs = {
    #             'action': project_action,
    #             'experiments': experiments,
    #             'runs': runs,
    #             'registrations': registrations,
    #             'participants': participants,
    #             'metas': ['evaluate'],
    #             'version': None # defaults to final state of federated grid
    #         }

    #         # kwargs.update(init_params)

    #         # PRODUCE TRAINING MESSAGE
    #         if app.config['IS_CLUSTER_MODE']:
    #             evaluate_operator = EvaluateProducerOperator(host=app.config["SYN_MQ_HOST"])
    #             result = evaluate_operator.process(project_id, kwargs)

    #             data = {"run_ids": result}

    #     # print(" [x] %r:%r" % (method.routing_key, body))
    #     logging.info(" [x] %r:%r" % (method.routing_key, body))
>>>>>>> 424bb037e4c2f8305c0cdd4b0948ff653a754632
        

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

    print("Completed_Consumer listening...")
    completed_consume = CompletedConsumerOperator(host=str2none(args.host))
    completed_consume.listen_message(start_hp_validations)