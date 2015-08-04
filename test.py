
import sys
import time

from constellations.node import Node
from constellations.basics.socketClientServer import SocketServer
from constellations.basics.socketClientServer import SocketClient


# The function to be supplied as callback to the socket server
def callbackfunction(message):
    print("handle: " + message)

server = SocketServer(50000, callbackfunction)
server.start()

SocketClient.send("localhost", 50000, "rnadom srting")


n = Node(50001)
SocketClient.send("localhost", 50001, "socket message")


time.sleep(1)
input("Press Enter to continue...")
sys.exit()