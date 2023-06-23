#!/usr/bin/python3
import subprocess

profile_cmd = './scripts/run_benchmark.sh profile:'
num_requests = 1000
access_count_arr = [1, 2, 4, 8, 16, 32, 64]
clients = ['anna', 'shredder']

def run_profile():
    # # create
    # subprocess.run(f'{profile_cmd}:1:create', shell=True)
    hot_key = 0
    
    for client_name in clients:
        start_key = 0
        for access_count in access_count_arr:
            # Cold
            cmd = f'{profile_cmd}{num_requests}:{client_name}:0:{start_key}:{access_count}'
            print('----------------------------------------------------------------------------')
            print(cmd)
            print('----------------------------------------------------------------------------')
            subprocess.run(cmd, shell=True)
            # Update start key, disable cache
            start_key += access_count * num_requests
            
            # Hot
            cmd = f'{profile_cmd}{num_requests}:{client_name}:1:{hot_key}:{access_count}'
            subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    run_profile()