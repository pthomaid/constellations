
import sys
import time

#from constellations.peer_node import PeerNode
from constellations.node import Node
from constellations.socket_transport import SocketTransport
from constellations import discovery
from constellations import gossip

# Socket Client and Server

"""
# The function to be supplied as callback to the socket server
def handler(message):
    print("handling: " + message)

servers = []
for i in range(0, 3):
    servers.append(SocketTransport())
    servers[i].receive(handler)

    print(servers[i].host)
    print(servers[i].port)

servers[0].send({"host":"localhost","port": servers[i].port}, "rnadom srting")
"""

# Nodes
def nodehandler(message):
    print("Node handling: " + message)

nn = 0
    
def gossiphandler(gossip):
    global nn
    print("Received new gossip: " + str(gossip) + str(nn))
    nn += 1
    
numberofnodes = 30
ns = []
gs = []

for i in range(0, numberofnodes):
    ns.append(Node())
    gs.append(gossip.Gossip())
    #ns[i].add_handler(nodehandler)
    discovery.add_discovery(ns[i])
    gs[i].add_gossip(ns[i])
    gs[i].register_handler(gossiphandler)
    print(ns[i].transport.host)
    print(ns[i].transport.port)

time.sleep(1)
gs[i].new_gossip(ns[i], "la")

#servers[0].send({"host":"localhost","port": ns[i].transport.port}, "rnadom srting")

for i in range(200):
    for i in range(0, numberofnodes):
        #print(ns[i].data.peers)
        print(str(ns[i].data.gossips) + "    " + str(ns[i].data.gossip_hops))
    print("===================\n===================")
    time.sleep(1)
    
"""
pn1 = PeerNode(n1)
pn2 = PeerNode(n2)
"""

time.sleep(1)
input("Press Enter to continue...")
sys.exit()