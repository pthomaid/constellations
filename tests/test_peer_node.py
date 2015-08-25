import unittest

import json
import time

from constellations import node
from constellations import message
from constellations import peer_node


class TestPeerNode(unittest.TestCase):

    # TODO Cleanup the server and ports properly in order to run multiple independent tests

    def setUp(self):
           
        # Creates nodes in ports 4500 to 4500+N-1
        N = 3
        self.nodes = []
        for i in range(4500, 4500+N):
            address = ["localhost", i]
            self.nodes.append(node.Node(host=address[0], port=address[1]))

        # Creates peer nodes in ports 5000 to 5000+N-1
        N = 3
        self.peer_nodes = []
        for i in range(5000, 5000+N):
            address = ["localhost", i]
            self.peer_nodes.append(peer_node.PeerNode(host=address[0], port=address[1]))

        addr = self.peer_nodes[0].data.me['address']
        for i in range(1, len(self.peer_nodes)):
            self.peer_nodes[i].data.peers["1"] = {}
            self.peer_nodes[i].data.peers["1"]["address"] = addr

    def tearDown(self):

        for n in self.nodes:
            n.stop()
        
        for pn in self.peer_nodes:
            pn.stop()
    
    def test_peer_nodes_address_sharing(self):
        
        for i in range(0, 10):
            for pn in self.peer_nodes:
                print(str(pn.data.me) + "\n" + str(pn.data.peers))
                print("----")
            print("--------------")
            time.sleep(2)

        # TODO Add relevant assertions
        # TODO assert that no exceptions were raised during running this test
        # TODO get rid of sleeps

    
    def test_new_peer_nodes_start_stop(self):
        
        addr = self.peer_nodes[0].data.me['address']

        # Creates new peer nodes in ports 5500 to 5500+N-1
        N = 3
        new_peer_nodes = []
        for i in range(5500, 5500+N):
            address = ["localhost", i]
            new_peer_nodes.append(peer_node.PeerNode(host=address[0], port=address[1]))
            
        for pn in new_peer_nodes:
            pn.data.peers["1"] = {}
            pn.data.peers["1"]["address"] = addr

        for i in range(0, 3):
            for pn in self.peer_nodes:
                print(str(pn.data.me) + "\n" + str(pn.data.peers))
                print("----")
            print("--------------")
            time.sleep(2)

        for pn in new_peer_nodes:
            pn.stop()

        for i in range(0, 7):
            for pn in self.peer_nodes:
                print(str(pn.data.me) + "\n" + str(pn.data.peers))
                print("----")
            print("--------------")
            time.sleep(2)

        # TODO Add relevant assertions
        # TODO assert that no exceptions were raised during running this test
        # TODO get rid of sleeps

if __name__ == "__main__":
    unittest.main()

