#!/usr/bin/python3
import sys
import subprocess

files = ['log_trigger.txt', 'latency.csv', 'detailed_latency.csv', 'exec_detailed_latency.csv', 'exec_latency.csv', 'throughput.csv']

## Fetch result from Cloudlab to local archive
def fetch(local_dir):
    with open('nodes.txt', 'r') as f:
        first_node = f.readline().rstrip()
    
    print(f'Fetch from remote node: {first_node}')
    first_node = first_node.replace('ssh', 'scp', 1)
    
    cmd_prefix = f'{first_node}:/users/jinwei/cluster/'
    for f in files:
        full_cmd = f'{cmd_prefix}{f} {local_dir}'
        print(full_cmd)
        subprocess.run(full_cmd, shell=True)

if __name__ == '__main__':
    ## Usage: ./scripts/fetch_data.py {local_dir}
    if len(sys.argv) < 2:
        print('Usage: ./scripts/fetch_data.py {local_dir}')
        exit(1)
        
    local_dir = sys.argv[1]
    fetch(local_dir)
