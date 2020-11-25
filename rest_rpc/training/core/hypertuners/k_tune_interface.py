#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in

# Libs

# Custom
from rest_rpc.training.core.hypertuners.k_tune_driver_script import start_generate_hp, start_training_hp, start_hp_validations
from rest_rpc import app
from rest_rpc.connection.core.utils import (
    RunRecords
)
from manager.completed_operations import CompletedConsumerOperator

##################
# Configurations #
##################

db_path = app.config['DB_PATH']
run_records = RunRecords(db_path=db_path)

n_samples=2

search_space = {
    'algorithm': 'FedProx',
    'rounds': {"type": "choice", "values": [1,1]},
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
    'precision_fractional': 3,
    'base_lr': 0.0005,
    'max_lr': 0.005,
}

kwargs = {
    "project_id": "test_project_1",
    "expt_id": "test_experiment_1",
    "n_samples": n_samples,
    "search_space": search_space
}

def test(loaded_kwargs, host):
    print("loaded_kwargs: ", loaded_kwargs)
    # loaded_kwargs =  "TRAINING COMPLETE -  test_project_1/test_experiment_1/optim_run_5c68e185-c28f-4159-8df4-2504ce94f4c7"
    status, project_expt_run = loaded_kwargs.split(' - ')
    project_id, expt_id, run_id = project_expt_run.strip().split('/')
    if status.split()[0] == 'TRAINING':
        print("STARTING hp validations")
        print(project_id, expt_id, run_id)
        start_hp_validations(project_id, expt_id, run_id, None)
    else:
        print("NOT TRAINING. pass..")

if __name__ == '__main__':
    # Generate hyperparameters
    start_generate_hp(kwargs)

    # Retrieved all runs from database.json
    retrieved_run = run_records.read_all()
    # Loop thru all runs with run_id prefixed with "optim" and send them to train queue
    for run in retrieved_run:
        if run['key']['run_id'].startswith('optim'):
            start_training_hp("test_project_1", "test_experiment_1", run['key']['run_id']) # send each hyperparamer config into the train queue


    # Logic to listen for completed task from buffer queue
    # and run evaluation based on the project_id, expt_id and run_id
    # ..

    print("Complete consumer listening..")
    completed_consume = CompletedConsumerOperator(host=app.config["SYN_MQ_HOST"])
    completed_consume.listen_message(test)
