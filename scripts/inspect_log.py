#!/usr/bin/python3
import argparse
import subprocess

role_dict = {'b': 'benchmark', 'm': 'management', 's': 'scheduler', 'f': 'function'}

def get_param(args):
    role = role_dict[args.type[0]]
    pod_name = subprocess.run(f'kubectl get pods -n default -l role={role} -o jsonpath="{{.items[{args.index}].metadata.name}}"', shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    
    container_name = None
    if role == 'benchmark' or role == 'function':
        container_name = role + '-' + args.cid
    
    if role == 'management':
        log_name = 'cluster/log_'
    else:
        log_name = 'cloudburst/log_'
    if role == 'function':
        log_name += 'executor'
    else:
        log_name += role
    log_name += '.txt'
    
    return pod_name, container_name, log_name, args.arg_suffix

def inspect_log(pod_name, container_name, log_name, suffix_args):
    if container_name:
        cmd = f'kubectl exec -it {pod_name} -n default -c {container_name} -- tail -f hydro/{log_name} {suffix_args}'
    else:
        cmd = f'kubectl exec -it {pod_name} -n default -- tail -f hydro/{log_name} {suffix_args}'
    print(cmd)
    subprocess.run(cmd, shell=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-t', '--type', nargs=1, type=str, dest='type', choices=['b', 'm', 's', 'f'], required=True)
    parser.add_argument('-i', '--pod_index', nargs='?', type=str, dest='index', default='0')
    parser.add_argument('-c', '--container_id', nargs='?', type=str, dest='cid', choices=['1', '2', '3', '4'], default='1')
    parser.add_argument('-a', nargs='?', type=str, dest='arg_suffix', default='')

    args = parser.parse_args()
    
    pod_name, container_name, log_name, suffix_args = get_param(args)

    inspect_log(pod_name, container_name, log_name, suffix_args)
    