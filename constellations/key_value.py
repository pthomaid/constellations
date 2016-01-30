
import sys
import time
import json
import random

from .node import Node
from .socket_transport import SocketTransport
from . import discovery

class Gossip_key_value():

    def __init__(self, gossip):
        self.gossip = gossip
        self.gossip.register_handler(self.handler)
        self.store = {}
        self.diffuse_probability = 0.1  # The probability that the node will gossip the data forward 
        self.store_probability = 0.1      # The probability that the node will store a key-value pair locally
        #N = 5
        #for i in range(N):
        #   self.store[i+index*N] = i+index*N
        #print(self.store)

    def get(self, key):
        if key in self.store:
            return self.store[key]
        else:
            return None
            
    def set(self, key, value):
        self.store[key] = value
        
    def distributed_set(self, key, value):
        if random.random() < self.store_probability:
            self.store[key] = value
        
        if random.random() < self.diffuse_probability:
            message = {}
            message["action"] = "set"
            message["key"] = key
            message["value"] = value
            self.gossip.new_gossip(json.dumps(message), hops=5)
            
    def handler(self, gossip):
        gossip = json.loads(gossip)
        if gossip["action"] == "get":        
            if gossip["key"] in self.store and not "value" in gossip:
                response = {}
                response["action"] = "get"
                response["key"] = gossip["key"]
                response["value"] = self.store[gossip["key"]]
                self.gossip.new_gossip(json.dumps(response), hops=5)
        
        elif gossip["action"] == "set":
            self.distributed_set(gossip["key"], gossip["value"])
