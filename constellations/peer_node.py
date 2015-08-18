
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
        self.add_handler(self.parse_address_list)
        self.add_act(self.share_my_address_list)

    def parse_address(self, s):
        m = message.parse(s)
        # TODO check if an addresses is already known
        self.data.me['address'] = m.to_address
        pid = self.peer_exists(m.from_address)
        if pid:
            pass
            #self.data.peers[pid]["message"] = m.message
        else:
            new_id = str(randint(1000, 9999))
            self.data.peers[new_id] = {}
            self.data.peers[new_id]['address'] = m.from_address
            #self.data.peers[new_id]["message"] = m.message

    def peer_exists(self, address):
        for key in self.data.peers:
            if self.data.peers[key]['address'] == address:
                return key
        return False

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

            time.sleep(randint(1,4))
       
    def parse_address_list(self, s):
        m = message.parse(s)
        if isinstance(m.message, dict):
            pid = self.peer_exists(m.message['peer']['address'])
            if pid:
                pass
                #self.data.peers[pid]["message"] = m.message
            else:
                new_id = str(randint(1000, 9999))
                self.data.peers[new_id] = {}
                self.data.peers[new_id]['address'] = m.message['peer']['address']
                #self.data.peers[new_id]["message"] = m.message['peer']['address']
     
    def share_my_address_list(self, context, data):
        while True:
            # TODO check if my address exists and is non empty
            my_address = data.me['address']
            m = message.Message()
            m.from_address = my_address

            for key in self.data.peers:
                peer_addr = self.data.peers[key]['address']
                m.to_address = peer_addr
                for key2 in self.data.peers:
                    if key != key2:
                        m.message['peer'] = {}
                        m.message['peer']['address'] = data.peers[key2]['address']
                        s = message.compose(m)
                        SocketClient.send(peer_addr[0], peer_addr[1], s)

            time.sleep(randint(1,4))

if __name__ == "__main__":

    p = PeerNode()

    import sys
    time.sleep(1)
    input("Press Enter to continue...")
    sys.exit()
