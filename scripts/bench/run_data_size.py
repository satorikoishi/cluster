#!/usr/bin/python3
import subprocess
import sys
import utils

## Example: ./scripts/bench/run_data_size.py ap

num_requests = 100
access_count_arr = [0,1,2,4,8]
data_size_arr = [8, 1024, 1024 * 10, 1024 * 100, 1024 * 1024]
duration_arr = [0]

def run_batch(bench_name, clients):
    func_cmd = f'./scripts/run_benchmark.sh {bench_name}'
    print(f'Test clients: {clients}')
    
    for data_size in data_size_arr:
        subprocess.run(f'{func_cmd}:1:create:{data_size}', shell=True)
        for client_name in clients:
            for access_count in access_count_arr:
                for duration in duration_arr:
                    cmd = f'{func_cmd}:{num_requests}:{client_name}:{access_count}:{data_size}:{duration}'
                    print(f'Access: {access_count}, Duration: {duration} us, {cmd}')
                    subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few args. Usage: ./scripts/bench/run_data_size.py {clients}')
        exit(1)
        
    func_name = 'data_size'
    clients = utils.parse_clients()
    
    run_batch(func_name, clients)
