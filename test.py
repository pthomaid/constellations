
import sys
import time

from constellations.node import Node
from constellations.basics.socketClientServer import SocketServer
from constellations.basics.socketClientServer import SocketClient

# Using the socket client and server
"""
# The function to be supplied as callback to the socket server
def callbackfunction(message):
    print("handle: " + message)

server = SocketServer(50000, callbackfunction)
server.start()

SocketClient.send("localhost", 50000, "rnadom srting")
"""

# Using the node
"""
def myhandler1(message):
    print("My handler1 received: " + message)

def myhandler2(message):
    print("My handler2 received: " + message)

n = Node()
n.add_handler(myhandler1)
n.add_handler(myhandler2)
n.start()

SocketClient.send("localhost", 50000, "lodpsdppsdpsdf")
time.sleep(2)
SocketClient.send("localhost", 50000, "second message")
"""

def myhandler(message):
    print("My handler1 received: " + message)

n1 = Node(50000)
n2 = Node(50001)
n1.add_handler(myhandler)
n2.add_handler(myhandler)
n1.start()
n2.start()

SocketClient.send("localhost", 50000, "lodpsdppsdpsdf")
time.sleep(2)
SocketClient.send("localhost", 50001, "second message")

time.sleep(1)
input("Press Enter to continue...")
sys.exit()