#!/usr/bin/python3
import subprocess
import sys
import utils

## Example: ./scripts/bench/run_ycsb.py ap

num_requests = 1000
workload_type = ['A', 'B', 'C', 'D', 'F']

def run_batch(bench_name, clients):
    func_cmd = f'./scripts/run_benchmark.sh {bench_name}'
    print(f'Test clients: {clients}')
    
    subprocess.run(f'{func_cmd}:1:create', shell=True)
    for client_name in clients:
        for w_type in workload_type:
            cmd = f'{func_cmd}:{num_requests}:{client_name}:{w_type}'
            print(f'{cmd}')
            subprocess.run(cmd, shell=True)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few args. Usage: ./scripts/bench/run_ycsb.py {clients}')
        exit(1)
        
    func_name = 'ycsb'
    clients = utils.parse_clients()
    
    run_batch(func_name, clients)
