import unittest

from constellations import config

class TestConfig(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_get_config(self):
        conf_dict = config.get()
        self.assertEqual(conf_dict['bind_port_range'], [40000, 40050])

    def test_get_config_wrong_path(self):
        config.path = ''    # Set a wrong filepath
        conf_dict = config.get()
        self.assertEqual(conf_dict['bind_port_range'], [50000, 50050])
