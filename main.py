#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import argparse
import logging
from subprocess import Popen

# Custom
from rest_rpc import app

##################
# Configurations #
##################

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.DEBUG)

###########
# Scripts #
###########

if __name__ == "__main__":
    # argparse if cluster....
        # app.config[IS_CLUSTER_MODE] = ...
        # trainoper
        # evaloper
    
    Popen(["python", "-m", "manager.completed_task_operations"])
    app.run(host="0.0.0.0", port=5000, debug=False)