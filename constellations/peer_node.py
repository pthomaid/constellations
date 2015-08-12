
import time
import json
import queue
from queue import Queue
from threading import Thread
from random import randint

from .basics.socketClientServer import SocketServer
from .basics.socketClientServer import SocketClient

from .node import Node


class Message:

    def __init__(self):
        self.from_address = ('', -1)
        self.to_address = ('', -1)
        self.message = {}

    def parse(self, s):
        # TODO Handle cases when the parsing goes wrong (exception, defaults values)
        s_dict = json.loads(s)
        self.from_address = s_dict['from']
        self.to_address = s_dict['to']
        self.message = s_dict['message']

    def jsonify(self):
        s = json.dumps(self)
        return s


class PeerNode:

    def __init__(self, node):
        self.node = node
        self.data = node.data

        self.node.add_handler(self.parse_address)
        self.node.add_act(self.share_my_address)

    def parse_address(self, s):
        m = Message()
        m.parse(s)
        # TODO check if adresses match already
        self.data.me['address'] = message.to_address
        self.node.data.peers[""+randint(1000, 9999)]['address'] = message.from_address

    def share_my_address(self, data):
        # TODO check if my address exists and is non empty
        my_address = data.me['address']
        m = Message()
        s = m.jsonify()

        for key in data.peers:
            peer_addr = data.peers[key]['address']
            SocketClient.send(peer_addr[0], peer_addr[0], s)