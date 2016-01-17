
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

def send_hi(node):

    message = {}
    message["type"] = "discovery"
    message["address"] = node.data.me['address']
    message = json.dumps(message)
    for host in c["known_hosts"]:
        for port in range(c['bind_port_range'][0], c['bind_port_range'][1]):
            SocketClient.send(host, int(port), message, False)
            time.sleep(0.01)

def receive_hi(node, message):
    message = json.loads(message)
    if message["type"] == "discovery":
        lock.acquire()
        pid = peer_exists(node.data.peers, message["address"])
        lock.release()
        if not pid:
            new_id = str(randint(100000, 999999))
            node.data.peers[new_id] = {}
            node.data.peers[new_id]['address'] = message["address"]

def share_my_address(node):
    peers = node.data.peers
    while True:
        message = {}
        message["type"] = "discovery"
        message["address"] = node.data.me["address"]
        message = json.dumps(message)
        
        lock.acquire()
        keys = list(peers.keys())
        lock.release()
        for key in keys:
            address = peers[key]["address"]
            node.transport.send_maybe((address[0], int(address[1])), message)
        time.sleep(randint(4,9))

def add_discovery(node, act=True, handler=True):
    if handler:
        node.add_handler(receive_hi)
    if act:
        node.add_act(send_hi)
        node.add_act(share_my_address)

    
