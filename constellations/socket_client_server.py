
import socket   # The socket module is a wrapper around native BSD sockets
from threading import Thread


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

    @staticmethod
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


