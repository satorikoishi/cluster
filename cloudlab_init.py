from fabric import Connection
from fabric.group import ThreadingGroup

init_cmd = 'git clone https://github.com/satorikoishi/cluster.git && ~/cluster/init.sh && ~/cluster/k8s.sh'

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
    
if __name__ == "__main__":
    pass