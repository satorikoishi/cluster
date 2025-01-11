#!/usr/bin/python3
import subprocess
import sys
import utils

## Example: ./scripts/bench/run_real_app.py ap

num_requests = 1000
app_list = ['auth', 'calc_avg', 'k_hop', 'file_replicator', 'list_traversal', 'user_follow']

def run_batch(bench_name, clients):
    func_cmd = f'./scripts/run_benchmark.sh {bench_name}'
    print(f'Test clients: {clients}')
    
    for app_name in app_list:
        subprocess.run(f'{func_cmd}:1:create:{app_name}', shell=True)
        for client_name in clients:
            cmd = f'{func_cmd}:{num_requests}:{client_name}:{app_name}'
            print(f'{cmd}')
            subprocess.run(cmd, shell=True)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few args. Usage: ./scripts/bench/run_real_app.py {clients}')
        exit(1)
        
    func_name = 'real_app'
    clients = utils.parse_clients()
    
    run_batch(func_name, clients)
