# Cloudlab Deployment

## Start experiment

- Profile: HYDRO
- Num_nodes: 7
- Image: Ubuntu 20.04

Wait for nodes to be ready.

## Initialize Kubernetes

Under cluster/ directory:

- Create file named **nodes.txt**, format like nodes-example.txt

- Copy SSH command into **nodes.txt**, one node per line

Then, run the following commands:

```shell
$ fab init
$ fab cluster
```

## Create cluster

SSH to node0

Under ~/cluster/

```shell
$ python3 -m hydro.cluster.create_cluster -m 1 -r 1 -f 1 -s 1 --us-ip {shredder node ip}
```

## Using Cloudburst Client
You can manually execute commands or use scripts.
### Manually execute commands

<!-- On node0

Run ``./cli_install.sh``, which will enter ~/cloudburst/

An example for bench trigger:

``
python3 cloudburst/client/benchmark_trigger.py {Node IP}:composition:10
`` -->
Directly use bench container as the client

```shell
$ k exec -it bench...(use Tab to autocomplete) -c benchmark-2 -- /bin/bash
```

In the container

```shell
$ cd hydro/cloudburst
$ export PYTHONPATH = $(pwd)
$ echo '{Benchmark Service IP}' > bench_ips.txt
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:{workload}:{num requests}:{args}
```

### Use scripts

SSH to node0

Under `~/cluster/` directory:
```shell
./scripts/run_benchmark.sh {workload}:{num requests}:{args}
```

## Inspect logs

### Use scripts

SSH to node0

Under `~/cluster/` directory:
```shell
Pod type: b / f / s / m

$ ./scripts/inspect_log.py -t {Pod type}

or

$ ./scripts/inspect_log.py -t {Pod type} -c {Container index} -i {Pod index} -a {Custom suffix}
```

## Workloads

### Micro

Before the first run, prepare data:

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:prepare:1
```

Run microbench, args: [KVS name, Workload, Length]

Workloads:

- read_single
- update_single

Lengths range from 10, 100, ..., to 1000000

Example: issue 100 requests to read arrays from Anna with length 10

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:micro:100:anna:read_single:10
```

### K-hop

Before the first run, prepare data:

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:k_hop:1:c
```

Run k-hop, args: k (k < 4, else the execution will consume too much time)

Example: issue 100 requests to perform 2-hop queries

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:k_hop:100:2
```

### List traversal

Before the first run, prepare data:
```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:list_traversal:1:create
```

Run `list_traversal`, args: KVS name, k

Example: issue 100 requests to perform 2-depth queries

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:list_traversal:100:anna:2
```

Run `list_traversal` JavaScript RPC version with shredder

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:list_traversal:100:shredder:2
```

### Social network

Before the first run, prepare data:
```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:list_traversal:1:create
```

Run `social_network`, args: KVS name, k

Example: issue 100 requests to perform 2-hop queries

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:social_network:100:anna:2
```

Run `social_network` all with shredder

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:social_network:100:shredder:2
```

Run `social_network` in hybrid mode

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:social_network:100:hybrid:2
```

Run `social_network` in tput mode and 1 client per benchmark thread.

```shell
$ python3 cloudburst/client/benchmark_trigger.py {Benchmark Pod IP}:social_network:1:hybrid:2:tput
```
