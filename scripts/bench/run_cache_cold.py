#!/usr/bin/python3
import subprocess
import sys
import utils

## Example: ./scripts/bench/run_cache_cold.py asr

num_requests = 1000
access_count_arr = [1,2,4,8,16,32]

def run_batch(bench_name, clients):
    func_cmd = f'./scripts/run_benchmark.sh {bench_name}'
    print(f'Test clients: {clients}')
    
    # run cold
    key_cold = 0
    for access_count in access_count_arr:
        cmd = f'{func_cmd}:{num_requests}:{key_cold}:{access_count}'
        print(f'Key start:{key_cold} Access: {access_count}, {cmd}')
        subprocess.run(cmd, shell=True)
        key_cold += access_count * num_requests
        
    # normal
    for client_name in clients:
        for access_count in access_count_arr:
            cmd = f'{func_cmd}:{num_requests}:{client_name}:{access_count}'
            print(f'Access: {access_count}, {cmd}')
            subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few args. Usage: ./scripts/bench/run_cache_cold.py {clients}')
        exit(1)
        
    func_name = 'cache_cold'
    clients = utils.parse_clients()
    
    run_batch(func_name, clients)
