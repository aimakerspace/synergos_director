#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import uuid
import argparse

# Libs
import ray
from ray import tune

# Custom
from rest_rpc import app
from rest_rpc.connection.core.utils import (
    RunRecords,
    ProjectRecords,
    ExperimentRecords,
    RegistrationRecords,
)
from rest_rpc.training.core.utils import (
    Poller
)

from manager.train_operations import TrainProducerOperator

##################
# Configurations #
##################

db_path = app.config['DB_PATH']
run_records = RunRecords(db_path=db_path)
project_records = ProjectRecords(db_path=db_path)
expt_records = ExperimentRecords(db_path=db_path)
registration_records = RegistrationRecords(db_path=db_path)

########################################
# HP Tuning Class - HPTuning #
########################################
def tune_trainable(config, checkpoint_dir=None):
    """
        trainable function for tune.run()
    """
    print("config: ", config)
    expt_id = config["expt_id"]
    project_id = config["project_id"]
    run_id = "optim_run_" + str(uuid.uuid4())
    search_space = config['search_space']

    ''':
        {'algorithm': 'FedProx', 
        'base_lr': 0.0005, 'criterion': 'MSELoss', 'delta': 0.0, 'epochs': 1, 'is_snn': False, 'l1_lambda': 0.0,
        'l2_lambda': 0.0, 'lr': 0.001, 'lr_decay': 0.1, 'lr_scheduler': 'CyclicLR', 'max_lr': 0.005, 'mu': 0.1,
        'optimizer': 'SGD', 'patience': 10, 'precision_fractional': 5, 'rounds': 'tune.choice([1,2,3,4,5])', 'seed': 42, 'weight_decay': 0.0}
    '''


    # Store records into database.json
    new_run = run_records.create(
        project_id=project_id, 
        expt_id=expt_id,
        run_id=run_id,
        details=config['search_space']
    )
    retrieved_run = run_records.read(
        project_id=project_id, 
        expt_id=expt_id,
        run_id=run_id
    )
    assert new_run.doc_id == retrieved_run.doc_id

def start_generate_hp(kwargs=None):
    """
        Start generate hyperparameters config
    """
    ray.shutdown()
    print("start generate hp")
    # ray.init(local_mode=True, ignore_reinit_error=True)
    ray.init(local_mode=True, num_cpus=1, num_gpus=0)

    num_samples = kwargs['n_samples'] # num of federated experiments (diff experiments diff hyperparameter configurations)
    gpus_per_trial=0

    ''':    
        kwargs = {'expt_id': 'test_experiment_1', 'project_id': 'test_project_1', n_samples: 3, 'search_space': {'algorithm': 'FedProx', 
        'base_lr': 0.0005, 'criterion': 'MSELoss', 'delta': 0.0, 'epochs': 1, 'is_snn': False, 'l1_lambda': 0.0,
        'l2_lambda': 0.0, 'lr': 0.001, 'lr_decay': 0.1, 'lr_scheduler': 'CyclicLR', 'max_lr': 0.005, 'mu': 0.1,
        'optimizer': 'SGD', 'patience': 10, 'precision_fractional': 5, 'rounds': {'type': 'choice', 'values': [1,2,3,4,5]}, 'seed': 42, 'weight_decay': 0.0}}
    '''

    # Mapping custom search space config into tune config
    search_space = kwargs['search_space']
    if search_space['rounds']['type'] == 'choice':
        search_space['rounds'] = tune.choice(search_space['rounds']['values'])

    result = tune.run(
        tune_trainable,
        config=kwargs,
        num_samples=num_samples,
    )

    print("hp kwargs: ", kwargs)

    return kwargs

def start_training_hp(project_id, expt_id, run_id):

    # The below train producer logic is extracted from the post function at rest_rpc/training/models.py

    # Populate grid-initialising parameters
    init_params = {'auto_align': True, 'dockerised': True, 'verbose': True, 'log_msgs': True} # request.json

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
    ###########################
    # Implementation Footnote #
    ###########################

    # [Cause]
    # Decoupling of MFA from training cycle is required. With this, polling is
    # skipped since alignment is not triggered

    # [Problems]
    # When alignment is not triggered, workers are not polled for their headers
    # and schemas. Since project logs are generated via polling, not doing so
    # results in an error for subsequent operations

    # [Solution]
    # Poll irregardless of alignment. Modify Worker's Poll endpoint to be able 
    # to handle repeated initiialisations (i.e. create project logs if it does
    # not exist,  otherwise retrieve)

    auto_align = init_params['auto_align']
    if not auto_align:
        poller = Poller(project_id=project_id)
        poller.poll(registrations)

    # Template for starting FL grid and initialising training
    kwargs = {
        'action': project_action,
        'experiments': experiments,
        'runs': runs,
        'registrations': registrations
    }
    kwargs.update(init_params)

    # output_payload = None #NOTE: Just added

    if app.config['IS_CLUSTER_MODE']:
        train_operator = TrainProducerOperator(host=app.config["SYN_MQ_HOST"])
        result = train_operator.process(project_id, kwargs)

        #return IDs of runs submitted
        resp_data = {"run_ids": result}
        print("resp_data: ", resp_data)    

def read_search_space_path(search_space_path):
    '''
    Parse search_space.json for project
    '''
    search_space = json.load(search_space_path)

    return search_space

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
        '--n_samples',
        dest='n_samples',
        help='Synergos HP Tuning',
        type=int,
        default=3
    )

    # reference where search_space json file is located
    parser.add_argument(
        '--search',
        dest='search_space_path',
        help='Search space path',
        type=str
    )
    
    args = parser.parse_args()

    '''
    search_space = {
        'algorithm': 'FedProx',
        'rounds': {"type": "choice", "values": [1,2,3,4,5]},
        'epochs': 1,
        'lr': 0.001,
        'weight_decay': 0.0,
        'lr_decay': 0.1,
        'mu': 0.1,
        'l1_lambda': 0.0,
        'l2_lambda': 0.0,
        'optimizer': 'SGD',
        'criterion': 'MSELoss',
        'lr_scheduler': 'CyclicLR',
        'delta': 0.0,
        'patience': 10,
        'seed': 42,
        'is_snn': False,
        'precision_fractional': 5,
        'base_lr': 0.0005,
        'max_lr': 0.005,
    }
    '''
    # search_space = read_search_space_path(args.search_space_path)

    '''
    kwargs = {
        "project_id": "test_project_1",
        "expt_id": "test_experiment_1",
        "n_samples": args.n_samples,
        "search_space": search_space,
    }

    start_generate_hp(kwargs)
    '''