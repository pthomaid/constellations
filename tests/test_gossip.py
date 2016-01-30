import unittest

import time

from constellations import node
from constellations import discovery

class TestDiscovery(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_discovery(self):
        nodes = [node.Node() for _ in range(10)]
        for n in nodes:
            discovery.add_discovery(n)
        
        time.sleep(10)  # Wait for the nodes to discover each other
        
        for n in nodes: # Assert that each node knows about the rest
            self.assertGreaterEqual(len(n.data.peer_set), len(nodes))
        
        '''
        for _ in range(1000):
            for n in nodes:
                print(n.transport.port)
                print(len(n.data.peer_set))
            print("")
            time.sleep(1)
        '''