#!/usr/bin/python3
import subprocess
import sys
import utils

## Example: ./scripts/bench/run_data_size_cold.py asr

num_requests = 100
access_count_arr = [1]
data_size_arr = [8, 1024, 1024 * 10, 1024 * 100, 1024 * 1024]
duration_arr = [0]

def run_batch(bench_name, clients):
    func_cmd = f'./scripts/run_benchmark.sh {bench_name}'
    print(f'Test clients: {clients}')
    
    # cold
    key_cold = 0
    for data_size in data_size_arr:
        subprocess.run(f'{func_cmd}:1:create:{data_size}', shell=True)
        for access_count in access_count_arr:
            cmd = f'{func_cmd}:{num_requests}:{key_cold}:{access_count}:{data_size}:0'
            print(f'Access: {access_count}, Key: {key_cold}, {cmd}')
            subprocess.run(cmd, shell=True)
            key_cold += access_count * num_requests

    # hot
    for data_size in data_size_arr:
        subprocess.run(f'{func_cmd}:1:create:{data_size}', shell=True)
        for access_count in access_count_arr:
            cmd = f'{func_cmd}:{num_requests}:anna:{access_count}:{data_size}:0'
            print(f'Access: {access_count}, {cmd}')
            subprocess.run(cmd, shell=True)
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few args. Usage: ./scripts/bench/run_data_size_cold.py {clients}')
        exit(1)
        
    func_name = 'data_size'
    clients = utils.parse_clients()
    
    run_batch(func_name, clients)
