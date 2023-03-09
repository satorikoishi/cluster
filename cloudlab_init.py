from fabric import Connection
from fabric.group import ThreadingGroup

init_cmd = 'git clone https://github.com/satorikoishi/cluster.git && ~/cluster/init.sh && ~/cluster/k8s.sh'
label_dict = {1:'general', 2:'routing', 3:'memory', 4:'function', 5:'scheduler', 6:'benchmark'}

class Node(object):
    def __init__(self, id, username, port, host):
        self.id = id
        self.username = username
        self.port = port
        self.host = host
    
    def home_addr(self):
        return f'{self.username}@{self.host}:/users/{self.username}'

def read_nodes(config_file = "nodes.txt"):
    nodes = []
    node_id = 0
    with open(config_file, 'r') as f:
        for line in f:
            res = line.split(' ')[1].strip().split('@')
            nodes.append(Node(node_id, res[0], 22, res[1]))
            node_id = node_id + 1
    # for node in nodes:
    #     print(f'Node id {node.id}, username {node.username}, port {node.port}, host {node.host}')
    return nodes

def get_host_connections():
    conns = []
    for node in read_nodes():
        host_c = Connection(host=node.host, user = node.username, port = node.port)
        conns.append(host_c)
    return conns

def batch_init():
    g_host = ThreadingGroup.from_connections(get_host_connections())
    
    print("Batch init start")
    g_host.run(init_cmd)
    print("Batch init finished")

def cluster_init():
    all_conns = get_host_connections()
    master_conn = all_conns[0]
    worker_conn = all_conns[1:]
    
    master_conn.run('sudo kubeadm init')
    master_conn.run('mkdir -p $HOME/.kube')
    master_conn.run('sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config')
    master_conn.run('sudo chown $(id -u):$(id -g) $HOME/.kube/config')
    
    join_cmd = master_conn.run('kubeadm token create --print-join-command')
    
    g_worker = ThreadingGroup.from_connections(worker_conn)
    g_worker.run('sudo ' + join_cmd.stdout)
    
    label_nodes(master_conn, worker_conn)

def label_nodes(master_conn, worker_conn):
    nodes = master_conn.run('kubectl get nodes').stdout.split('\n')
    node_id = 1
    for line in nodes:
        if 'node' + str(node_id) in line:
            node = line.split(' ')[0]
            master_conn.run(f'kubectl label nodes {node} role={label_dict[node_id]}')
            node_id = node_id + 1
    
if __name__ == "__main__":
    pass