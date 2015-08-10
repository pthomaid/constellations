
import time
import json
import queue
from queue import Queue
from threading import Thread
from random import randint

from .basics.socketClientServer import SocketServer
from .basics.socketClientServer import SocketClient

from .node import Node


class CommNode:

    def __init__(self, node):
        self.node = node
        self.data = node.data

        self.node.add_handler(self.parse_address)
        self.node.add_act(self.share_my_address)

    def parse_address(self, message):
        mdict = json.loads(message)
        address = mdict['address']
        self.node.data.others[""+randint(1000, 9999)]['address'] = address

    def share_my_address(self, data):
        # TODO check if my address exists and is non empty
        my_address = data.me['address']
        saddr = json.dumps(data.me.address)

        for key in data.peers:
            addr = data.peers[key]['address']
            SocketClient.send(addr[0], addr[1], saddr)