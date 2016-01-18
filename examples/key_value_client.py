
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
            ans = self.answer_queue.get(timeout=10)  # 10 seconds timeout
            key_found = ans[0]
            value_found = ans[1]
            while  key_found != key or key_found == None:
                ans = self.answer_queue.get(timeout=10)
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

kvc1 = Key_value_client()
kvc2 = Key_value_client()
time.sleep(10)

#key = 67
#print("key = " + str(key) + " value = " + str(kvc.distributed_get(key)))
#key = 72
#print("key = " + str(key) + " value = " + str(kvc.distributed_get(key)))
#key = 90
#print("key = " + str(key) + " value = " + str(kvc.distributed_get(key)))
#key = 13
#print("key = " + str(key) + " value = " + str(kvc.distributed_get(key)))

kvc1.distributed_set(1, 5)
kvc1.distributed_set(2, 10)
kvc1.distributed_set(3, 15)
kvc1.distributed_set(4, 20)
kvc1.distributed_set(5, 25)
time.sleep(10)
print("key = " + str(1) + " value = " + str(kvc2.distributed_get(1)))
print("key = " + str(2) + " value = " + str(kvc2.distributed_get(2)))
print("key = " + str(3) + " value = " + str(kvc2.distributed_get(3)))
print("key = " + str(4) + " value = " + str(kvc2.distributed_get(4)))
print("key = " + str(5) + " value = " + str(kvc2.distributed_get(5)))

'''
for i in range(200):
    print(str(mynode.data.gossips))
    print("===================\n===================")
    time.sleep(0.5)
'''

time.sleep(1)
input("Press Enter to continue...")
sys.exit()