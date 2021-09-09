# Synergos Director

Main job orchestrator for a synergos cluster.

![Synergos Components](./docs/images/syncluster_setup.png)

*Setting up Synergos Cluster for complex workloads*

In federated learning, it is important to establish a secured grid, where all orchestrator(s) and participants can reside in, and communicate accordingly for complex federated workflows. However, this is often easier said than done, due to a multitude of deployment conditions & configurations to consider. That's where `Synergos` and its respective components come in. 

The ideas behind `Synergos` are simple: 
- MODULARITY - Plug-&-play methodology for assembling your ideal grid architecture
- AUTOMATION - All complexities involving federated orchestration are to be abstracted
- SIMPLICITY - Deploy & execute in a single command

TL;DR, We want users to be able to configure & deploy their federated endeavours with ease & confidence.

<br>

**Synergos Director** is one of the core components necessary to scale up your Synergos workflow!

![Synergos Grid Configurations](./docs/images/synergos_modules.png)

*X-raying Synergos' core components*

Under the hood, we see that every feature embedded within each Synergos component is modularized as well. This allows users to activate or de-activate certain functionalities depending on their deployment setup.

In addition to having all functions as that of [Synergos TTP](https://github.com/aimakerspace/synergos_ttp), it serves to ease the process of parallelizing multiple jobs across multiple federated grids.

---

## Installation

Synergos Director has been dockerized for easy component-based deployment. 

```
# Download source repository
git clone https://github.com/aimakerspace/synergos_director
cd ./synergos_director

# Initialize & update all submodules
git submodule update --init --recursive
git submodule update --recursive --remote

# Build director image
docker build -t synergos_director:syncluster --label "syncluster_director" .

# Start containerized service
docker run --rm 
    -p <PORT>:5000      
    -v <PATH-TO-DATA>:/orchestrator/data        # <-- Mount for data access
    -v <PATH-TO-OUTPUTS>:/orchestrator/outputs  # <-- Mount for outputs access
    -v <PATH-TO-MLFLOGS>:/mlflow                # <-- Mount for MLFlow outputs
    --name director_syncluster 
    synergos_director:syncluster          
        --id director_syncluster        
        --logging_variant <LOGGER-VARIANT> <LOGGER-HOST> <SYSMETRIC-PORT> 
        --queue <MQ-VARIANT> <MQ-HOST> <MQ-PORT>
        --censored                              # <-- optional
        --debug                                 # <-- optional
```

- `<PORT>` - Port on which Synergos Director is served
- `<PATH-TO-DATA>` - User's custom volume on which data is to be stored 
- `<PATH-TO-OUTPUTS>` - User's custom volume on which outputs are to be stored
- `<PATH-TO-MLFLOGS>` - User's custom volume on which MLFlow logs are to be stored
- `<LOGGER-VARIANT>` - Logger backend deployed (i.e. `"graylog"` or `"basic"`)
    - `<LOGGER-HOST>` - If Synergos Logger was deployed, specify logger's host
    - `<SYSMETRIC-PORT>` - If Synergos Logger was deployed, specify logger's allocated sysmetric port. A sysmetric port is the port allocated for logging system resource usage for any synergos component within the same deployment setting/grid.
- `<MQ-VARIANT>` - Message queue backend deployed (only `"rabbitmq"` accepted for now)
    - `<MQ-HOST>` - Specify Synergos MQ's host. This is a mandatory declaration, since Synergos Director orchestratrates jobs across multiple grids.
    - `<MQ-PORT>` - Synergos MQ's allocated port

An example of a launch command is as follows:

```
docker run --rm 
    -p 5001:5000      
    -v /synergos_demos/orchestrator/data/:/director/data      
    -v /synergos_demos/orchestrator/outputs/:/director/outputs      
    -v /synergos_demos/orchestrator/mlflow/:/mlflow 
    --name director_syncluster 
    synergos_director:syncluster          
        --id director_syncluster        
        --logging_variant graylog 172.30.0.4 9300 
        --queue rabbitmq 172.17.0.4 5672
```

> Note: Only 1 **Synergos Director** instance is required in a `SynCluster` grid!

---
<br>

## Further Resources

You can view the guides for running:
- [Synergos Basic Standalone Grid i.e. local](https://docs.synergos.ai/BasicRunLocal.html)
- [Synergos Basic Distributed Grid i.e. across multiple devices](https://docs.synergos.ai/BasicRunDistributed.html)
- [Synergos Cluster Distributed Grid i.e. across multiple devices](https://docs.synergos.ai/ClusterRunDistributed.html)
- [Example Datasets and Jupyter Notebooks](https://github.com/aimakerspace/Synergos/tree/master/examples)