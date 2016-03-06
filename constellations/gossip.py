
import time
import json
import random
from random import randint

from . import config
from constellations.socket_transport import SocketClient

max_gossip_hops = 30

class Gossip_data():
    def __init__(self, text, hops=max_gossip_hops):
        self.text = text
        self.hops = hops

    def __str__(self):
        return str(self.text) + " hops:" + str(self.hops)
        
class Gossip():
    """Implementation of the gossip protocol (https://en.wikipedia.org/wiki/Gossip_protocol)
    using a Node as the communication layer
    
    Params:
        node:
    
    """
    
    def __init__(self, node, fanout=3):
        self.node = node
        self.gossip_list = []   # list of gossips (see class Gossip above)
        self.node.add_handler(self.receive_gossip)
        self.node.add_act(self.send_gossip)    
        self.gossip_handlers = []
        self.fanout = fanout

    def get_gossip_index(self, text):
        for i, gossip in enumerate(self.gossip_list):
            if gossip.text == text:
                return i
        return None

    def register_handler(self, handler):
        """Registers a handler that is called when a new gossip arrives
        Args:
            handler: a function with signature f(gossip)
    """
        self.gossip_handlers.append(handler)
    
    def notify(self, gossip):
        for handler in self.gossip_handlers:
            handler(gossip)
                    
    def new_gossip(self, text, hops=max_gossip_hops):
        self.gossip_list.append(Gossip_data(text, hops))
        #self.node.data.gossip_hops[gossip] = hops
        # TODO: Use a separate thread for this so that handlers don't block this thread
        self.notify(text)

    def send_gossip(self, node):
        peers = self.node.data.peers
        while True:
            if(len(self.gossip_list) == 0 or len(peers) == 0):
                time.sleep(1)
                continue

            gossip_index = randint(0, len(self.gossip_list)-1)              # Select a random gossip
            gossip = self.gossip_list[gossip_index]
            gossip.hops -= 1                                                                                 # Decrement the number of hops
            if gossip.hops <= 0:                                                                          # Remove expired gossips 
                self.gossip_list.remove(gossip)
                continue

            peer_keys = random.sample(list(peers.keys()), self.fanout)     # Select *fanout* random peers

            for peer_key in peer_keys:
                message = {}                                                                                         # Assemble message
                message["type"] = "gossip"
                message["value"] = gossip.text
                message["gossip_hops"] = gossip.hops
                message = json.dumps(message)
            
                address = peers[peer_key]["address"]                                          # Send
                self.node.transport.send_maybe((address[0], int(address[1])), message)
                time.sleep(0.1)

    def receive_gossip(self, node, message):
        message = json.loads(message)
        if message["type"] == "gossip":
            text = message["value"]
            hops = message["gossip_hops"]
            index = self.get_gossip_index(text)
            if index is None:
                self.new_gossip(text, hops)                                                         # Received a new gossip
            else:
                self.gossip_list[index].hops = min(self.gossip_list[index].hops, hops)      # Update existing gossip hops

def add_gossip(node):
    g = Gossip()
    node.add_handler(g.receive_gossip)
    node.add_act(g.send_gossip)
