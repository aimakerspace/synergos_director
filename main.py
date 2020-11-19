#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import argparse
import logging
from subprocess import Popen, PIPE

# Custom
from rest_rpc import app

##################
# Configurations #
##################

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

####################
# Helper Functions #
####################

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

###########
# Scripts #
###########

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()

    # Cluster variant activation
    parser.add_argument(
        '--cluster',
        dest='is_cluster',
        help='Activate cluster mode - choices: True/False',
        type=str,
        nargs='?',
        choices=['t','f', 'true', 'false', 'True', 'False'],
        default='True'
        )

    parser.add_argument(
        '--mqhost',
        dest='mqhost',
        help='Synergos_MQ server host',
        default=None,
        type=str
    )
    
    args = parser.parse_args()
    
    if str2bool(args.is_cluster):
        app.config["IS_CLUSTER_MODE"] = True
    else:
        app.config["IS_CLUSTER_MODE"] = False

    if args.mqhost:
        app.config["SYN_MQ_HOST"] = args.mqhost
    else:
        app.config["SYN_MQ_HOST"] = None

    # Run completed_task consumer as subprocess
    # Popen(
    #     ["python", "-m", "manager.completed_operations",\
    #      "--host", f"{app.config['SYN_MQ_HOST']}"],
    #      shell=False,
    #      stdout=PIPE,
    #      stderr=PIPE
    #      )

    # Run flask
    app.run(host="0.0.0.0", port=5000, debug=False)