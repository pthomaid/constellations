import unittest

import json
import time

from constellations import node
from constellations import message
from constellations import peer_node


class TestPeerNode(unittest.TestCase):

    def setUp(self):
        
        N = 3
        self.nodes = []
        addresses = []
        for i in range(4500, 4500+N):
            address = ["localhost", i]
            addresses.append(address)
            self.nodes.append(node.Node(host=address[0], port=address[1]))

        # Creates peer nodes in ports 5000 to 5000+N-1
        N = 3
        self.peer_nodes = []
        addresses = []
        for i in range(5000, 5000+N):
            address = ["localhost", i]
            addresses.append(address)
            self.peer_nodes.append(peer_node.PeerNode(host=address[0], port=address[1]))

    def tearDown(self):

        for n in self.nodes:
            n.stop()
        
        for pn in self.peer_nodes:
            pn.stop()

    # TODO Cleanup the server and ports properly in order to run multiple independent tests
    # SetUp, TearDown?
    """
    def testNode(self):
        p = node.Node()
        p.stop()

    def testNode2(self):
        p = node.Node()
        p.stop()

    def testPeerNode(self):
        address = ["localhost", 5000]
        p = peer_node.PeerNode(host=address[0], port=address[1])
        self.assertEqual(p.data.me["address"], address)
        p.stop()
    """
    
    def test_peer_nodes_address_sharing(self):
        
        addr = self.peer_nodes[0].data.me['address']

        self.peer_nodes[1].data.peers["1"] = {}
        self.peer_nodes[1].data.peers["1"]["address"] = addr

        self.peer_nodes[2].data.peers["1"] = {}
        self.peer_nodes[2].data.peers["1"]["address"] = addr

        for i in range(0, 10):
            for pn in self.peer_nodes:
                print(str(pn.data.me) + "\n" + str(pn.data.peers))
                print("----")
            print("--------------")
            time.sleep(2)

        # TODO Add relevant assertions
        # TODO assert that no exceptions were raised during running this test
        # TODO get rid of sleeps
    

