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

<!-- On node0

Run ``./cli_install.sh``, which will enter ~/cloudburst/

An example for bench trigger:

``
python3 cloudburst/client/benchmark_trigger.py {Node IP}:composition:10
`` -->
Directly use bench container as client

``
$ k exec -it bench...(use Tab to autocomplete) -c benchmark-2 -- /bin/bash
``

In container

``
$ cd hydro/cloudburst
$ export PYTHONPATH = $(pwd)
$ echo '{Benchmark Service IP}' > bench_ips.txt
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:{workload}:{num requests}:{args}
``

## Workloads

### Micro

Before first run, prepare data

``
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:prepare:1
``

Run microbench, args: [Workload, Length]

Workloads:

- read_single
- update_single

Length from 10, 100, ... to 1000000

Example, which issues 100 requests to read arrays, length of which is 10

``
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:micro:100:read_single:10
``

### K-hop

Before first run, prepare data

``
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:k_hop:1:c
``

Run k-hop, args: k (k < 4, else the execution will consume too much time)

Example, which issues 100 requests to do 2-hop queries

``
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:k_hop:100:2
``