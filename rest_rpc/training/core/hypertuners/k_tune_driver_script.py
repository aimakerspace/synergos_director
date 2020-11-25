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
from manager.evaluate_operations import EvaluateProducerOperator


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

    '''
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

    '''    
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


def start_hp_validations(project_id, expt_id, run_id, participant_id):
    # {"test_project_1": {"action": "regress", "auto_align": true, "dockerised": true, "experiments": [{"created_at": "2020-11-24 08:32:56", "key": {"expt_id": "test_experiment_1", "project_id": "test_project_1"}, "model": [{"activation": "", "is_input": true, "l_type": "Linear", "structure": {"bias": true, "in_features": 10, "out_features": 31}}, {"activation": "", "is_input": true, "l_type": "Linear", "structure": {"bias": true, "in_features": 31, "out_features": 1}}]}], "log_msgs": true, "metas": ["evaluate"], "participants": ["test_participant_1", "test_participant_3"], "registrations": [{"created_at": "2020-11-24 08:33:03", "key": {"participant_id": "test_participant_1", "project_id": "test_project_1"}, "link": {"registration_id": "ab4536b62e2f11eba9d30242ac110003"}, "participant": {"created_at": "2020-11-24 08:33:01", "f_port": 5000, "host": "172.17.0.4", "id": "test_participant_1", "key": {"participant_id": "test_participant_1"}, "log_msgs": true, "port": 8020, "verbose": true}, "project": {"action": "regress", "created_at": "2020-11-24 08:32:53", "incentives": {"tier_1": [], "tier_2": []}, "key": {"project_id": "test_project_1"}}, "relations": {"Alignment": [{"created_at": "2020-11-24 08:33:09", "evaluate": {"X": [], "y": []}, "key": {"participant_id": "test_participant_1", "project_id": "test_project_1"}, "link": {"alignment_id": "aeb42c3a2e2f11ebb3d00242ac110003", "registration_id": "ab4536b62e2f11eba9d30242ac110003", "tag_id": "ac31cc7e2e2f11eb8f5e0242ac110003"}, "train": {"X": [], "y": []}}], "Participant": [], "Project": [], "Tag": [{"created_at": "2020-11-24 08:33:05", "evaluate": [["evaluate"]], "key": {"participant_id": "test_participant_1", "project_id": "test_project_1"}, "link": {"registration_id": "ab4536b62e2f11eba9d30242ac110003", "tag_id": "ac31cc7e2e2f11eb8f5e0242ac110003"}, "predict": [], "train": [["train"]]}]}, "role": "guest"}, {"created_at": "2020-11-24 08:33:03", "key": {"participant_id": "test_participant_3", "project_id": "test_project_1"}, "link": {"registration_id": "ab4ef43a2e2f11ebbf1d0242ac110003"}, "participant": {"created_at": "2020-11-24 08:33:01", "f_port": 5000, "host": "172.17.0.5", "id": "test_participant_3", "key": {"participant_id": "test_participant_3"}, "log_msgs": true, "port": 8020, "verbose": true}, "project": {"action": "regress", "created_at": "2020-11-24 08:32:53", "incentives": {"tier_1": [], "tier_2": []}, "key": {"project_id": "test_project_1"}}, "relations": {"Alignment": [{"created_at": "2020-11-24 08:33:09", "evaluate": {"X": [], "y": []}, "key": {"participant_id": "test_participant_3", "project_id": "test_project_1"}, "link": {"alignment_id": "aeb176c02e2f11ebb3d00242ac110003", "registration_id": "ab4ef43a2e2f11ebbf1d0242ac110003", "tag_id": "ac39427e2e2f11eb99800242ac110003"}, "train": {"X": [], "y": []}}], "Participant": [], "Project": [], "Tag": [{"created_at": "2020-11-24 08:33:05", "evaluate": [["evaluate"]], "key": {"participant_id": "test_participant_3", "project_id": "test_project_1"}, "link": {"registration_id": "ab4ef43a2e2f11ebbf1d0242ac110003", "tag_id": "ac39427e2e2f11eb99800242ac110003"}, "predict": [], "train": [["train"]]}]}, "role": "host"}], "runs": [{"algorithm": "FedProx", "base_lr": 0.0005, "created_at": "2020-11-24 08:33:32", "criterion": "MSELoss", "delta": 0.0, "epochs": 1, "is_snn": false, "key": {"expt_id": "test_experiment_1", "project_id": "test_project_1", "run_id": "optim_run_85a50653-aaed-4817-af27-afc7339dd826"}, "l1_lambda": 0.0, "l2_lambda": 0.0, "lr": 0.001, "lr_decay": 0.1, "lr_scheduler": "CyclicLR", "max_lr": 0.005, "mu": 0.1, "optimizer": "SGD", "patience": 10, "precision_fractional": 3, "rounds": 2, "seed": 42, "weight_decay": 0.0}], "verbose": true, "version": null}}
    """ Triggers FL inference for specified project-experiment-run
        combination within a PySyft FL grid. 
        Note: Participants have the option to specify additional datasets
                here for prediction. However all prediction sets will be
                collated into a single combined prediction set to facilitate
                prediction. Also, all prediction tags submitted here will
                override any previously submitted prediction tags registered
                for a specified project. This is to prevent accumulation of 
                unsynced dataset tags (w.r.t participant's node). Hence, if
                a participant wants to expand their testing datasets by 
                declaring new tags, the onus is on them to declare all of it
                per submission.

        Sample payload:

        {
            "auto_align": true,
            "dockerised": true
        }
    """
    # Populate grid-initialising parameters
    # init_params = {'auto_align': True, 'dockerised': True, 'verbose': True, 'log_msgs': True} # request.json

    # Retrieves expt-run supersets (i.e. before filtering for relevancy)
    retrieved_project = project_records.read(project_id=project_id)
    print("retrieved_project: ", retrieved_project)
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

    # Retrieve all relevant participant IDs, collapsing evaluation space if
    # a specific participant was declared
    participants = [
        record['participant']['id'] 
        for record in registrations
    ] if not participant_id else [participant_id]

    # Template for starting FL grid and initialising validation
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
    
    if app.config['IS_CLUSTER_MODE']:
        evaluate_operator = EvaluateProducerOperator(host=app.config["SYN_MQ_HOST"])
        result = evaluate_operator.process(project_id, kwargs)

        data = {"run_ids": result}