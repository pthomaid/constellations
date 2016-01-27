
import time
import json
from random import randint
from threading import Lock

from . import config
from .socket_transport import SocketClient

class Discovery():

    def __init__(self):
        self.config = config.get()
        self.lock = Lock()
        self.my_addresses = []
        self.peers = []

    def peer_exists(self, peers, address):
        #lock.acquire()
        for key in peers:
            if peers[key]['address'] == address:
                return key
        #lock.release()
        return False

    def merge_lists(self, list1, list2):
        for address in list2:
            if not address in list1:
                list1.append(address)
        return list1
        
    def send_discovery(self, node):
        while True:
            message_dict = {}
            message_dict['type'] = 'discovery'
            #message_dict['from'] = node.data.me['address']
            for host in self.config["known_hosts"]:
                for port in range(self.config['bind_port_range'][0], self.config['bind_port_range'][1]):
                    peer_address = [host, port]
                    self.lock.acquire()
                    message_dict['peers'] = self.peers
                    message_dict['to'] = peer_address
                    message = json.dumps(message_dict)
                    self.lock.release()
                    SocketClient.send(host, int(port), message, False)
                time.sleep(0.1)
                #print("dadadadadadadadadadad")
            time.sleep(100)

    def send_all_to_all(self, node):
        while True:
            message_dict = {}
            message_dict['type'] = 'discovery'
            for peer in self.peers:
                message_dict['peers'] = self.peers
                message_dict['to'] = peer
                message = json.dumps(message_dict)
                SocketClient.send(peer[0], int(peer[1]), message, False)
                time.sleep(0.1)
            time.sleep(3)
            
    def receive_discovery(self, node, message):
        #print(message)
        message_dict = json.loads(message)
        if message_dict['type'] == 'discovery':
            self.my_addresses = self.merge_lists(self.my_addresses, [message_dict['to']])
            self.lock.acquire()
            self.peers = self.merge_lists(self.peers, message_dict['peers'])
            self.peers = self.merge_lists(self.peers, [message_dict['to']])
            #self.send_all_to_all()
            self.lock.release()
            #print('self.peers')
            #print(self.peers)
            node.data.peer_set = list(self.peers)

    '''
    response_dict = {}
    response_dict['type'] = 'discovery_response'
    response_dict['from'] = message_dict['to']
    response_dict['to'] = message_dict['from']
    response = json.dumps(response_dict)
    SocketClient.send(response_dict['to'][0], int(response_dict['to'][1]), response, False)
        
    def receive_discovery_response(self, node, message):
        message_dict = json.loads(message)
        if message_dict['type'] == 'discovery_response':
            self.lock.acquire()
            pid = self.peer_exists(node.data.peers, message_dict['from'])
            self.lock.release()
            if not pid:
                new_id = str(randint(100000, 999999))
                node.data.peers[new_id] = {}
                node.data.peers[new_id]['address'] = message_dict['from']
  '''
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
    d = Discovery()
    if handler:
        node.add_handler(d.receive_discovery)
        #node.add_handler(d.receive_discovery_response)
    if act:
        node.add_act(d.send_discovery)
        #node.add_act(share_my_address)
        node.add_act(d.send_all_to_all)

    
