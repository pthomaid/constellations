import unittest

import json

from constellations import peer_node


class TestPeerNode(unittest.TestCase):

    def testMessageJson(self):
        m = peer_node.Message()

        d = {}
        d["from"] = ["localhost", 50000]
        d["to"] = ["localhost", 50001]
        d["message"] = "lorem ipsum"
        s = json.dumps(d)

        m.parse(s)

        self.assertEqual(m.from_address, ["localhost", 50000])
        self.assertEqual(m.to_address, ["localhost", 50001])
        self.assertEqual(m.message, "lorem ipsum")

if __name__ == '__main__':
    unittest.main()