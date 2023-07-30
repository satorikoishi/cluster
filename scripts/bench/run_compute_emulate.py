#!/usr/bin/python3
import subprocess
import sys
import utils

## Example: ./scripts/bench/run_compute_emulate.py asr

num_requests = 10000
access_count_arr = [0,1,2,4,8,16,32]
duration_arr = [0,10,100,1000,10000]

def run_batch(bench_name, clients):
    func_cmd = f'./scripts/run_benchmark.sh {bench_name}'
    print(f'Test clients: {clients}')
    
    for client_name in clients:
        for access_count in access_count_arr:
            for duration in duration_arr:
                cmd = f'{func_cmd}:{num_requests}:{client_name}:{access_count}:{duration}'
                print(f'Access: {access_count}, Duration: {duration} us, {cmd}')
                subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few args. Usage: ./scripts/bench/run_compute_emulate.py {clients}')
        exit(1)
        
    func_name = 'compute_emulate'
    clients = utils.parse_clients()
    
    run_batch(func_name, clients)
