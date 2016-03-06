
import sys
import time
import json

from constellations.socket_transport import SocketTransport
from constellations import discovery
from constellations.key_value import Gossip_key_value
from constellations.key_value_client import Key_value_client
from constellations.node import Node
from constellations.gossip import Gossip

"""Using the gossip key value store, using a client
"""

kvc = Key_value_client()

print(kvc.distributed_get("key1"))
print(kvc.distributed_get("key2"))

time.sleep(1)
input("Press Enter to continue...")
sys.exit()