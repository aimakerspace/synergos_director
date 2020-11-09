#!/usr/bin/env python

####################
# Required Modules #
####################



# Generic/Built-in
import threading
import asyncio
import os

# Libs

# Custom
from .train_operations import TrainOperator
from .evaluate_operations import EvaluateOperator
from .completed_task_operations import CompletedTaskOperator


HOST = None

train_operator = TrainOperator()
evaluate_operator = EvaluateOperator()

# temporarily place consumer run here
def start_consumer(host=HOST):
    CompletedTaskOperator(host).listen_message()

consumer_thread = threading.Thread(target=start_consumer)
consumer_thread.start()