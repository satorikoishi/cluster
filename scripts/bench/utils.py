import sys

def parse_clients():
    clients = []
    
    if 'a' in sys.argv[1]:
        clients.append('anna')      # Add anna
    if 's' in sys.argv[1]:
        clients.append('shredder')  # Add shredder
    if 'p' in sys.argv[1]:
        clients.append('pocket')    # Add pocket mock
    if 'r' in sys.argv[1]:
        clients.append('arbiter')   # Add arbiter
        
    return clients