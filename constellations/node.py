
import time
import queue
from queue import Queue
from threading import Thread
from random import randint

from .basics.socketClientServer import SocketServer
from .basics.socketClientServer import SocketClient


class Data:

    def __init__(self):
        self.me = {}
        self.peers = {}


class Node(Thread):
    """ A Node combines an input server with a queue and a list of handlers """

    def __init__(self, host='', port=50000):
        super(Node, self).__init__()
        self.daemon = True  # Makes the thread exit when the main program exits

        # TODO pick another port if the first one is already bound
        # TODO add the handler and acts lists implementations (think about the semantics and abstractions)
        # TODO make Node be a thread or use its own thread

        self.data = Data()
        self.data.me['address'] = (host, port)

        # A queue to place incoming messages until they are handled
        self.message_queue = Queue()

        # Add the put method of the message_queue as callback to the server
        self.server = SocketServer(self.message_queue.put, host, port)

        # handlers are functions that accept the messages from the queue as input
        self.handlers = []
        self.acts = []

        self.running = True
        self.server.start()

    def add_handler(self, func):
        # TODO check if func supports the message argument (is this possible?)
        self.handlers.append(func)

    def add_act(self, func):
        # TODO check if func supports the data argument (is this possible?)
        self.acts.append(func)

    def run(self):
        """Gets one message at a time from message_queue and passes it to the registered handlers"""
        while self.running:
            try:
                # Waits for 3 seconds, otherwise throws `Queue.Empty`
                next_item = self.message_queue.get(True, 3)
            except queue.Empty:
                next_item = None

            # Passes the next queue item to all the registered handlers (TODO should I clone the message?)
            if next_item is not None:
                for h in self.handlers:
                    h(next_item)

            # Run the acts one by one
            # TODO run in separate threads if required
            for a in self.acts:
                a(self.data)


if __name__ == "__main__":

    def myhandler1(message):
        print("My handler1 received: " + message)

    def myhandler2(message):
        print("My handler2 received: " + message)

    n = Node()
    n.add_handler(myhandler1)
    n.add_handler(myhandler2)
    n.start()

    SocketClient.send("localhost", 50000, "lodpsdppsdpsdf")

    time.sleep(2)

    SocketClient.send("localhost", 50000, "second message")

    import sys
    time.sleep(1)
    input("Press Enter to continue...")
    sys.exit()


