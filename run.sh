#!/usr/bin/env bash

########################################
# Step 0: Define simulation conditions #
########################################

grid_count = $1
worker_per_grid = $2

######################################################
# Step 1: Push changes in sub-component repositories #
######################################################

# A. Commit changes in Synergos Algorithm

# B. Commit changes in Synergos Archive

# C. Commit changes in Synergos Logger

# D. Commit changes in Synergos Manager

# E. Commit changes in Synergos Rest

#############################################################################
# Step 2: Rebuild containerized components (i.e. Director, TTP(s), Workers) #
#############################################################################

# A. Rebuild Synergos Worker

# B. Rebuild Synergos TTP

# C. Rebuild Synergos Director

#############################################################################
# Step 3: Run all containerized components (i.e. Director, TTP(s), Workers) #
#############################################################################

# Start Director
docker run \
    -p 5000:5000 \
    -p 8080:8080 \
    -v /home/aisg/Desktop/synergos_demos/ttp_data/:/director/data \
    -v /home/aisg/Desktop/synergos_demos/ttp_outputs/:/director/outputs \
    -v /home/aisg/Desktop/synergos_demos/mlflow_test/:/director/mlflow \
    --name director_syncluster \
    synergos_director:syncluster 
        --id director_syncluster \
        --logging_variant graylog 172.30.0.4 9300 \
        --queue rabbitmq 172.17.0.5 5672 \
        --debug \
        --censored

# Start all TTP(s)
for grid_idx in {0..${grid_count}}
do
ttp_name = ttp_syncluster_${grid_idx}
docker run \
    -p 5001:5000 \
    -p 8081:8080 \
    -v /home/aisg/Desktop/synergos_demos/ttp_data/:/ttp/data \
    -v /home/aisg/Desktop/synergos_demos/ttp_outputs/:/ttp/outputs \
    -v /home/aisg/Desktop/synergos_demos/mlflow_test/:/ttp/mlflow \
    --name ${ttp_name} \
    synergos_ttp:syncluster \
        --id ttp_syncluster_${} \
        --logging_variant graylog 172.30.0.4 9300 \
        --queue rabbitmq 172.17.0.5 5672 \
        --debug \
        --censored
done

# Start all Workers
docker run \
    -v /home/aisg/Desktop/synergos_demos/datasets/:/worker/data \ 
    -v /home/aisg/Desktop/synergos_demos/outputs_1:/worker/outputs \ 
    --name worker_1 \
    synergos_worker:syncluster \
        --id test_worker_1 \
        --logging_variant graylog 172.19.0.4 9400 \ 
        --debug \ 
        --censored

docker run \
    -v /home/aisg/Desktop/synergos_demos/datasets/:/worker/data \
    -v /home/aisg/Desktop/synergos_demos/outputs_2:/worker/outputs \
    --name worker_2 \
    synergos_worker:syncluster \
        --id test_worker_2 \
        --logging_variant graylog 172.19.0.4 9400 \
        --debug \
        --censored