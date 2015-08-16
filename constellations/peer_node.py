
import time
import json
import queue
from queue import Queue
from threading import Thread
from random import randint

from .socket_client_server import SocketServer
from .socket_client_server import SocketClient
from .node import Node
from . import message


class PeerNode(Node):

    def __init__(self, host='', port=50000):
        super().__init__(host, port)

        self.add_handler(self.parse_address)
        self.add_act(self.share_my_address)

    def parse_address(self, s):
        print("Peer node received " + s)
        m = message.parse(s)
        # TODO check if an addresses is already known
        self.data.me['address'] = m.to_address
        new_id = str(randint(1000, 9999))
        self.data.peers[new_id] = {}
        self.data.peers[new_id]['address'] = m.from_address

    def share_my_address(self, context, data):
        while True:
            # TODO check if my address exists and is non empty
            my_address = data.me['address']
            m = message.Message()
            m.from_address = my_address
            m.message = "message in a bottle"

            for key in self.data.peers:
                peer_addr = self.data.peers[key]['address']
                m.to_address = peer_addr
                s = message.compose(m)
                SocketClient.send(peer_addr[0], peer_addr[1], s)

            time.sleep(3)

if __name__ == "__main__":

    p = PeerNode()

    import sys
    time.sleep(1)
    input("Press Enter to continue...")
    sys.exit()
