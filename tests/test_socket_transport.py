
import unittest

import json
import time

from constellations import socket_transport


def callback(message):
    print("Received " + message)

class TestSocketTransport(unittest.TestCase):

# TODO Cleanup the server and ports properly in order to run multiple independent tests

    def setUp(self):
        pass

    def tearDown(self):
        pass
    
    def test_socket_transport_server_start_stop(self):
        address = {'host':'', 'port':5000}
        st = socket_transport.SocketTransport(address)
        st.receive(callback)
        time.sleep(3)
        st.close()
        time.sleep(3)
        # TODO assert that everything is closed, is this possible

    def test_socket_transport_server_port_busy(self):
        address1 = {'host':'', 'port':5001}
        address2 = {'host':'', 'port':5001}
        st1 = socket_transport.SocketTransport(address1)
        st1.receive(callback)
        st2 = socket_transport.SocketTransport(address2)
        st2.receive(callback)
        print(st1.host + ":" + str(st1.port))
        print(st2.host + ":" + str(st2.port))

if __name__ == "__main__":
    unittest.main()

