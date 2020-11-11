# Synergos Director

Main job orchestrator for a synergos cluster.

## Using the package locally
1. Clone this repository

2. Change directory into the cloned repository and build a docker image of Synergos Directory with
`docker build -t synergos_director:alpha_0.0.0 .`

3. In CLI, pull the docker image for Synergos Message Exchange with
```
docker pull registry.aisingapore.net/fedlearn/synergos_mq:alpha_0.0.0
```

4. In CLI, start the container for the Synergos Message Exchange with
```
docker run -p 15672:15672 -p 5672:5672 --name syn_mq \
registry.aisingapore.net/fedlearn/synergos_mq:alpha_0.0.0
```

5. Run `docker inspect bridge` to identify the IPv4 of syn_mq container within the docker internal network.
    e.g `172.17.0.4`

6. Assuming that relevant worker containers (e.g `worker_1` and `worker_2`) are running, start the 
```
docker run -it --rm -p 5000:5000 --link worker_1 --link worker_2 --name syn_dir_run synergos_director:alpha_0.0.0 --mqhost <Synergos Message Exchange IP add>
```

7. The network is now ready, and Synergos UI can be access from the browser at `localhost:5000`