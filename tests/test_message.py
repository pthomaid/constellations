import unittest

import json
import time

from constellations import node
from constellations import message
from constellations import peer_node

class TestMessage(unittest.TestCase):

    def test_message_json_conversion(self):
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

