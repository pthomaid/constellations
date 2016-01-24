import time
import sys

from constellations.node import Node
from constellations import discovery
from constellations.gossip import Gossip_node
from constellations.key_value import Gossip_key_value

numberofnodes = 20
stores = []

for i in range(0, numberofnodes):
    n = Node()
    discovery.add_discovery(n)
    print(n.transport.host)
    print(n.transport.port)
    stores.append(Gossip_key_value(Gossip_node(n)))

for i in range(10000):
    for i in range(0, numberofnodes):
        #print(ns[i].data.peers)
        #print(*gs[i].gossip_list)
        print(*stores[i].store.items())
    print("===================\n===================")
    time.sleep(0.5)

time.sleep(1)
input("Press Enter to continue...")
sys.exit()