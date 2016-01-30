
import sys
import time

from constellations.socket_transport import SocketTransport
from constellations import discovery
from constellations.key_value import Gossip_key_value
from constellations.key_value_client import Key_value_client
from constellations.node import Node
from constellations.gossip import Gossip

"""Using the gossip key value store
"""

# Create a few gossip key-value nodes
numberofnodes = 6
stores = [0]*numberofnodes
for i in range(0, numberofnodes):
    n = Node()
    discovery.add_discovery(n)
    stores[i] = Gossip_key_value(Gossip(n))

for _ in range(10):
    for s in stores:
        print(s.gossip.node.data.peers)
        print("")
    time.sleep(2)

# Set some random values
stores[3].set("key1", "value1")
stores[5].set("key2", "value2")

# Create a client
client = Key_value_client()
# Use the client to get the values
value1 = client.distributed_get("key1")
value2 = client.distributed_get("key2")
print(value1)
print(value2)

time.sleep(1)
input("Press Enter to continue...")
sys.exit()