
import sys
import time

from constellations.node import Node
from constellations.basics.socketClientServer import SocketServer
from constellations.basics.socketClientServer import SocketClient


"""
# The function to be supplied as callback to the socket server
def callbackfunction(message):
    print("handle: " + message)

server = SocketServer(50000, callbackfunction)
server.start()

SocketClient.send("localhost", 50000, "rnadom srting")
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


time.sleep(1)
input("Press Enter to continue...")
sys.exit()