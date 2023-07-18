#!/usr/bin/python3
import subprocess
import sys

## Example: ./scripts/bench/run_facebook_social.py asr

num_requests = 10000
percent_arr = [0,5,10,50,100]
depth_arr = [1,2,4,8,16]

def run_batch(bench_name, clients):
    func_cmd = f'./scripts/run_benchmark.sh {bench_name}'
    print(f'Test clients: {clients}')
    
    for client_name in clients:
        for percent in percent_arr:
            for depth in depth_arr:
                cmd = f'{func_cmd}:{num_requests}:{client_name}:{percent}:{depth}'
                print(f'Percent: {percent}, depth: {depth}, {cmd}')
                subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Too few args. Usage: ./scripts/bench/run_compute_emulate.py {clients}')
        exit(1)
        
    func_name = 'compute_emulate'
    clients = []
    
    if 'a' in sys.argv[1]:
        clients.append('anna')      # Add anna
    if 's' in sys.argv[1]:
        clients.append('shredder')  # Add shredder
    if 'r' in sys.argv[1]:
        clients.append('arbiter')   # Add arbiter
    
    run_batch(func_name, clients)
