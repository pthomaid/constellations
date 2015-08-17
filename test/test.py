import unittest

import json
import time

from constellations import node
from constellations import message
from constellations import peer_node


class TestPeerNode(unittest.TestCase):

    def testMessageJson(self):
        d = {}
        d["from"] = ["localhost", 50000]
        d["to"] = ["localhost", 50001]
        d["message"] = "lorem ipsum"
        s = json.dumps(d)

        m = message.parse(s)

        self.assertEqual(m.from_address, ["localhost", 50000])
        self.assertEqual(m.to_address, ["localhost", 50001])
        self.assertEqual(m.message, "lorem ipsum")

        s_composed = message.compose(m)
        self.assertEqual(s, s_composed)

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

    """
    def testTwoPeerNodes(self):
        address1 = ["localhost", 5000]
        address2 = ["localhost", 5001]
        p1 = peer_node.PeerNode(host=address1[0], port=address1[1])
        p2 = peer_node.PeerNode(host=address2[0], port=address2[1])

        p2.data.peers["1"] = {}
        p2.data.peers["1"]["address"] = address1

        time.sleep(20)

        p1.stop()
        p2.stop()

        # TODO assert that no exceptions were raised during running this test
    """

    def testNPeerNodes(self):
        N = 3
        pnodes = []
        addresses = []
        for i in range(5000, 5000+N):
            address = ["localhost", i]
            addresses.append(address)
            pnodes.append(peer_node.PeerNode(host=address[0], port=address[1]))

        pnodes[1].data.peers["1"] = {}
        pnodes[1].data.peers["1"]["address"] = addresses[0]

        pnodes[2].data.peers["1"] = {}
        pnodes[2].data.peers["1"]["address"] = addresses[0]

        for i in range(0, 10):
            for pn in pnodes:
                print(str(pn.data.me) + "\n" + str(pn.data.peers))
                print("----")
            print("--------------")
            time.sleep(2)

        for pn in pnodes:
            pn.stop()

        # TODO assert that no exceptions were raised during running this test
