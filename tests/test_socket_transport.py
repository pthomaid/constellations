
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
        addr = {'host':'', 'port':5000}
        st = socket_transport.SocketTransport(addr)
        st.receive(callback)
        time.sleep(5)
        st.close()
        # TODO assert that everything is closed, if possible
    
    def test_socket_transport_server_port_busy(self):
        addr1 = {'host':'', 'port':5001}
        addr2 = {'host':'', 'port':5001}
        st1 = socket_transport.SocketTransport(addr1)
        st1.receive(callback)
        st2 = socket_transport.SocketTransport(addr2)
        st2.receive(callback)
        print(st1.host + ":" + str(st1.port))
        print(st2.host + ":" + str(st2.port))
        time.sleep(5)
        st1.close()
        st2.close()
    
    def test_socket_transport_server_client(self):
        addr = {'host':'', 'port':5010}
        st = socket_transport.SocketTransport(addr)
        actual_addr = {'host':st.host, 'port':st.port}
        st.receive(callback)
        time.sleep(5)
        message = "I am not a message"
        st.send(actual_addr, message)
        st.close()
    

if __name__ == "__main__":
    unittest.main()

