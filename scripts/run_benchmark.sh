#!/bin/bash

# Define variables
NAMESPACE="default" # Replace with the actual namespace where the pod is running
TRIGGER_CONTAINER_NAME="benchmark-2" # Replace with the actual container name
WORKLOAD="$(echo $1 | cut -d':' -f1)" # Extract workload from the first argument
NUM_REQUESTS="$(echo $1 | cut -d':' -f2)" # Extract number of requests from the first argument
ARGS="$(echo $1 | cut -d':' -f3-)" # Extract remaining arguments from the first argument

# Get the pod name
POD_NAME=$(kubectl get pods -n $NAMESPACE -l role=benchmark -o jsonpath="{.items[0].metadata.name}")

# Get the benchmark service IP
BENCHMARK_SVC_IP=$(kubectl get svc -n $NAMESPACE benchmark-service -o jsonpath="{.spec.clusterIP}")

# Get the benchmark pod IP
POD_IP=$(kubectl get pods -n $NAMESPACE $POD_NAME -o jsonpath="{.status.podIP}")

# Print parameters
echo -e "benchmark pod name: $POD_NAME\nbenchmark service ip: $BENCHMARK_SVC_IP\npod ip: $POD_IP"
echo -e "workload: $WORKLOAD\nnum requests: $NUM_REQUESTS\nargs: $ARGS"

# Prepare trigger arguments
if [ -z "$ARGS" ]; then
    ARGS="$POD_IP:$WORKLOAD:$NUM_REQUESTS"
else
    ARGS="$POD_IP:$WORKLOAD:$NUM_REQUESTS:$ARGS"
fi

# Run command in trigger container
echo "kubectl exec trigger..."
kubectl exec -i $POD_NAME -n $NAMESPACE -c $TRIGGER_CONTAINER_NAME -- bash << EOF
cd hydro/cloudburst
export PYTHONPATH=\$(pwd)
if [ ! -f bench_ips.txt ]; then
  echo $BENCHMARK_SVC_IP > bench_ips.txt
fi
python3 cloudburst/client/benchmark_trigger.py $ARGS
EOF

# Copy benchmark results to the current directory
echo "kubectl cp benchmark results..."
kubectl cp -n $NAMESPACE -c $TRIGGER_CONTAINER_NAME $POD_NAME:/hydro/cloudburst/log_trigger.txt ./log_trigger.txt
kubectl cp -n $NAMESPACE -c $TRIGGER_CONTAINER_NAME $POD_NAME:/hydro/cloudburst/latency.csv ./latency.csv
kubectl cp -n $NAMESPACE -c $TRIGGER_CONTAINER_NAME $POD_NAME:/hydro/cloudburst/exec_latency.csv ./exec_latency.csv
kubectl cp -n $NAMESPACE -c $TRIGGER_CONTAINER_NAME $POD_NAME:/hydro/cloudburst/throughput.csv ./throughput.csv

echo done!
