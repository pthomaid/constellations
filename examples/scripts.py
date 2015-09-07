
import sys
import time

#from constellations.peer_node import PeerNode
from constellations.node import Node
from constellations.socket_transport import SocketTransport


# Socket Client and Server

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


# Nodes
def nodehandler(message):
    print("Node handling: " + message)

ns = []

for i in range(0, 10):
    ns.append(Node())
    ns[i].add_handler(nodehandler)
    
    print(ns[i].transport.host)
    print(ns[i].transport.port)

servers[0].send({"host":"localhost","port": ns[i].transport.port}, "rnadom srting")

"""
pn1 = PeerNode(n1)
pn2 = PeerNode(n2)
"""

time.sleep(1)
input("Press Enter to continue...")
sys.exit()