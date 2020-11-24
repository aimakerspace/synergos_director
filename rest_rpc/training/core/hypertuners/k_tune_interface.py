#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in

# Libs

# Custom
from rest_rpc.training.core.hypertuners.k_tune_script import start_generate_hp, start_training_hp
from rest_rpc import app
from rest_rpc.connection.core.utils import (
    RunRecords
)


##################
# Configurations #
##################

db_path = app.config['DB_PATH']
run_records = RunRecords(db_path=db_path)

n_samples=3

search_space = {
    'algorithm': 'FedProx',
    'rounds': {"type": "choice", "values": [1,2]},
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


