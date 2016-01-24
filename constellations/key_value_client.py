
import sys
import time
import json
import threading
import queue

from constellations.node import Node
from constellations.socket_transport import SocketTransport
from constellations import discovery
from constellations import gossip

class Key_value_client():

    def __init__(self):
        self.node = Node()
        self.gossip = gossip.Gossip_node(self.node)
        discovery.add_discovery(self.node)
        self.gossip.register_handler(self.gossip_handler)
        self.event = threading.Event()
        self.answer_queue = queue.Queue()

    def distributed_get(self, key):
        qu = {}
        qu["action"] = "get"
        qu["key"] = key
        self.gossip.new_gossip(json.dumps(qu))
        self.event.clear()
        try:
            ans = self.answer_queue.get(timeout=15)  # 10 seconds timeout
            key_found = ans[0]
            value_found = ans[1]
            while  key_found != key or key_found == None:
                ans = self.answer_queue.get(timeout=15)
                key_found = ans[0]
                value_found = ans[1]
            return value_found
        except:
            return None
 
    def distributed_set(self, key, value):
        qu = {}
        qu["action"] = "set"
        qu["key"] = key
        qu["value"] = value
        self.gossip.new_gossip(json.dumps(qu))

    def gossip_handler(self, gossip):
        gossip = json.loads(gossip)
        if gossip["action"] == "get" and  "key" in gossip and "value" in gossip:
            self.answer_queue.put((gossip["key"], gossip["value"]))
