
import time
import json
from random import randint
from threading import Lock

from . import config
from .socket_transport import SocketClient

c = config.get()

lock = Lock()

def peer_exists(peers, address):
    #lock.acquire()
    for key in peers:
        if peers[key]['address'] == address:
            return key
    #lock.release()
    return False

def send_discovery(node):
    message_dict = {}
    message_dict['type'] = 'discovery'
    message_dict['from'] = node.data.me['address']
    for host in c["known_hosts"]:
        for port in range(c['bind_port_range'][0], c['bind_port_range'][1]):
            peer_address = [host, port]
            message_dict['to'] = peer_address
            message = json.dumps(message_dict)
            SocketClient.send(host, int(port), message, False)
            time.sleep(0.01)

def receive_discovery(node, message):
    message_dict = json.loads(message)
    if message_dict['type'] == 'discovery':    
        response_dict = {}
        response_dict['type'] = 'discovery_response'
        response_dict['from'] = message_dict['to']
        response_dict['to'] = message_dict['from']
        response = json.dumps(response_dict)
        SocketClient.send(response_dict['to'][0], int(response_dict['to'][1]), response, False)
        
def receive_discovery_response(node, message):
    message_dict = json.loads(message)
    if message_dict['type'] == 'discovery_response':
        lock.acquire()
        pid = peer_exists(node.data.peers, message_dict['from'])
        lock.release()
        if not pid:
            new_id = str(randint(100000, 999999))
            node.data.peers[new_id] = {}
            node.data.peers[new_id]['address'] = message_dict['from']

'''
def share_my_address(node):
    peers = node.data.peers
    while True:
        message_dict = {}
        message_dict['type'] = "discovery"
        message_dict['from'] = node.data.me['address']
        
        lock.acquire()
        keys = list(peers.keys())
        lock.release()
        for key in keys:
            peer_address = peers[key]["address"]
            message_dict['to'] = peer_address
            message = json.dumps(message_dict)
            node.transport.send_maybe((peer_address[0], int(peer_address[1])), message)
        time.sleep(randint(60,120))
'''

def add_discovery(node, act=True, handler=True):
    if handler:
        node.add_handler(receive_discovery)
        node.add_handler(receive_discovery_response)
    if act:
        node.add_act(send_discovery)
        #node.add_act(share_my_address)

    
