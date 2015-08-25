import unittest

import json
import time

from constellations import node
from constellations import message


class TestNode(unittest.TestCase):

    # TODO Cleanup the server and ports properly in order to run multiple independent tests

    def setUp(self):
           
        # Creates nodes in ports 4500 to 4500+N-1
        N = 3
        self.nodes = []
        for i in range(4500, 4500+N):
            address = ["localhost", i]
            self.nodes.append(node.Node(host=address[0], port=address[1]))

    def tearDown(self):

        for n in self.nodes:
            n.stop()
    
    def test_assign_node_to_taken_port(self):

        addr = self.nodes[0].data.me['address']

        n = node.Node(addr[0], addr[1])

        # TODO Assert the assigned address
        # TODO Assert no exception thrown

