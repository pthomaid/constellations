
import socket   # The socket module is a wrapper around native BSD sockets
from threading import Thread
from random import randint

from . import config

class SocketTransport():

    def __init__(self):
        self.running = True

        # The socket() function returns a socket object whose methods implement the various socket system calls
        # Using default arguments, see the socket module documentation for options
        self.s = socket.socket()
        
        # Socket operations will raise a timeout exception if the timeout period value has elapsed before the operation has completed
        self.s.settimeout(3)    # seconds
        
        self.host = ''         # '' means all available interfaces
        self.port = -1         # will be set in the bind function

        # Attempts to bind the server, preferably on the specified address
        self.server_bind()

    def receive(self, callback):
        self.server_callback = callback
        self.server_thread = Thread(target=self.server_listen, daemon=True)
        self.server_thread.start()

    def server_listen(self):
        # Sets ut the socket to listen for incoming connections
        self.s.listen(1)
        try:
            while self.running:    # Always serve
                try:
                    #print("listening socket " + str(self.s))
                    conn, addr = self.s.accept()
                    data = conn.recv(1024)
                    # Convert the input message to a string and pass it to the message handler
                    self.server_callback(data.decode('UTF-8'))
                    # Send reply, is it neccessary?
                    conn.sendall(bytes("ack", 'UTF-8'))
                    conn.close()
                except (socket.timeout):
                    pass
                except (socket.error):
                    break
        finally:
            self.close()

    def server_bind(self):
        c = config.get()
        succesful_bind = False
        temp_port = c['bind_port_range'][0]
        times = 10
        try_counter = times
        while not succesful_bind:
            try:
                # Binds the socket to the address specified, the format of the address depends on address family
                self.s.bind((self.host, temp_port))
                succesful_bind = True
                break
            except (socket.error):
                print("The port was taken, trying another")
                succesful_bind = False
            try_counter -= 1
            if(try_counter == 0):
                raise socket.error("The socket server could not be bound after " + str(times) + "times")
            temp_port = randint(c['bind_port_range'][0], c['bind_port_range'][1])
        self.port = temp_port

    def send(self, address, message):
        SocketClient.send(address['host'], address['port'], message)

    def close(self):
        self.running = False
        # TODO read about setsockopt and options
        # TODO find a way to programmatically stop reading and close the socket
        #self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # Close the socket
        self.s.close()

class SocketServer(Thread):
    """A threaded server that forwards the incoming messages to a supplied callback"""

    def __init__(self, callback, host='', port=50000):
        super(SocketServer, self).__init__()
        self.daemon = True  # Makes the thread exit when the main program exits

        # The socket() function returns a socket object whose methods implement the various socket system calls
        # Using default arguments, see the socket module documentation for options
        self.s = socket.socket()

        self.host = ''      # Means all available interfaces
        self.port = port
        self.callback = callback

    def run(self):

        # Binds the socket to the address specified, the format of the address depends on address family
        self.s.bind((self.host, self.port))

        # Sets ut the socket to listen for incoming connections
        self.s.listen(1)

        try:
            while True:    # Always serve
                conn, addr = self.s.accept()

                data = conn.recv(1024)

                # Convert the input message to a string and pass it to the message handler
                self.callback(data.decode('UTF-8'))

                # Send reply
                conn.sendall(bytes("ack", 'UTF-8'))

                conn.close()

        finally:

            # TODO read about setsockopt and options
            # TODO find a way to programmatically stop reading and close the socket

            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Close the socket
            self.s.close()


class SocketClient:
    """Sends string messages via a socket address"""

    def send(host, port, message):
        response = ""
        try:
            # Create the socket object
            s = socket.socket()

            s.connect((host, port))

            # Convert the message to bytes and send
            s.sendall(bytes(message, 'UTF-8'))

            # Receive the response
            response = s.recv(1024)
        except TypeError:
            print("TypeError while sending: " + message)
        finally:
            s.close()

        return response.decode('UTF-8')

# Usage & testing
if __name__ == "__main__":

    import sys
    import time

    # The function to be supplied as callback to the socket server
    def callbackfunction(message):
        print("handle: " + message)

    server = SocketServer(50000, callbackfunction)
    server.start()

    SocketClient.send("localhost", 50000, "rnadom srting")

    time.sleep(2)
    input("Press Enter to continue...")
    sys.exit()


