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
        
        for _ in range(1000):
            for n in nodes:
                print(n.data.peers)
                print("")
            time.sleep(1)