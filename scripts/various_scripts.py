
import sys
import time

from constellations.socket_transport import SocketTransport
from constellations import discovery
from constellations.key_value import Gossip_key_value
from constellations.key_value_client import Key_value_client
from constellations.node import Node
from constellations.gossip import Gossip

def using_the_socket_transport():
    """Using the socketTransport
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


    
using_the_socket_transport()

time.sleep(1)
input("Press Enter to continue...")
sys.exit()