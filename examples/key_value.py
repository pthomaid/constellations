
import sys
import time
import json
import random

from constellations.node import Node
from constellations.socket_transport import SocketTransport
from constellations import discovery
from constellations import gossip

class Datastore():

    def __init__(self, index, node, gossip):
        self.node = node
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
            self.set(gossip["key"], gossip["value"])

numberofnodes = 20
ns = []
gs = []
ds = []

for i in range(0, numberofnodes):
    ns.append(Node())
    gs.append(gossip.Gossip_node(ns[i]))
    ds.append(Datastore(i, ns[i], gs[i]))
    
    #ns[i].add_handler(nodehandler)
    discovery.add_discovery(ns[i])
    print(ns[i].transport.host)
    print(ns[i].transport.port)

'''
time.sleep(10)
qu = {}
qu["key"] = 36
gs[i].new_gossip(ns[i], json.dumps(qu))
'''

for i in range(10000):
    for i in range(0, numberofnodes):
        #print(ns[i].data.peers)
        #print(*gs[i].gossip_list)
        print(*ds[i].store.items())
    print("===================\n===================")
    time.sleep(0.5)

time.sleep(1)
input("Press Enter to continue...")
sys.exit()