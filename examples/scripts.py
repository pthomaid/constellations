
import sys
import time

from constellations.socket_transport import SocketTransport
from constellations import discovery
from constellations.key_value import Gossip_key_value
from constellations.key_value_client import Key_value_client
from constellations.node import Node
from constellations.gossip_node import Gossip_node

"""Using the socketTransport
"""

"""
# The function to be supplied as callback to the socket server
def handler(message):
    print("handling: " + message)

servers = []
for i in range(0, 3):
    t = SocketTransport()
    t.receive(handler)
    print(t.host)
    print(t.port)
    
    servers.append(t)

servers[0].send({"host":"localhost","port": servers[i].port}, "rnadom srting")
"""

"""Using the gossip key value store
"""

# Create a few gossip key-value nodes
numberofnodes = 10
stores = []
for i in range(0, numberofnodes):
    n = Node()
    discovery.add_discovery(n)
    print(n.transport.host)
    print(n.transport.port)
    stores.append(Gossip_key_value(Gossip_node(n)))

for _ in range(15):
    for n in stores:
        print(n.gossip.node.data.peers)
        print("")
    time.sleep(2)
    
# Set some random values
stores[3].set("key1", "value1")
stores[7].set("key2", "value2")

# Create a client
client = Key_value_client()

time.sleep(5)

# Use the client to get the values
value1 = client.distributed_get("key1")
value2 = client.distributed_get("key2")
print(value1)
print(value2)

time.sleep(1)
input("Press Enter to continue...")
sys.exit()