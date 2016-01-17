import unittest

from constellations import datastore

class TestDataStore(unittest.TestCase):

    def test_value_set_get(self):
        ds = datastore.SimpleDataStore()
        ds.set("key1", 1)
        ds.set("key2", 2)

        n1 = ds.get("key1")
        n2 = ds.get("key2")
        
        self.assertEqual(n1, 1)
        self.assertEqual(n2, 2)

