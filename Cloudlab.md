# Cloudlab Deployment

## Start experiment

- Profile: HYDRO
- Num_nodes: 7
- Image: Ubuntu 20.04

Wait for nodes ready

## Init k8s

Under cluster/

Create file named **nodes.txt**, format like nodes-example.txt

Copy SSH command into **nodes.txt**, one node per line

Then, run ``fab init``, ``fab cluster``

## Create cluster

SSH to node0

Under ~/cluster/

Run ``python3 -m hydro.cluster.create_cluster -m 1 -r 1 -f 1 -s 1``

## Using Cloudburst Client

On node0

Run ``./cli_install.sh``, which will enter ~/cloudburst/

An example for bench trigger:

``
python3 cloudburst/client/benchmark_trigger.py {Node IP}:composition:10
``
