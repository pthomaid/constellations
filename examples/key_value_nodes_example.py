import time
import sys

from constellations.node import Node
from constellations import discovery
from constellations import gossip
from constellations.key_value import Datastore

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