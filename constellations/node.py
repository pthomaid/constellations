
import time
import queue
from queue import Queue
from threading import Thread
from random import randint

from .basics.socketClientServer import SocketServer
from .basics.socketClientServer import SocketClient


class Data:

    def __init__(self, data=None):
        self.me = {}
        self.peers = {}
        self.message_queue = Queue()

    def add_me(self, data):
        # TODO Investigate more elegant ways to copy the data
        for key in data:
            self.me[key] = data[key]

    def add_peer(self, data):
        # TODO Pattern-match existing peers before creating a new one
        new_name = "temp_" + randint(1000, 9999)
        self.peers[new_name] = {}
        for key in data:
            self.peers[new_name][key] = data[key]


class Node(Thread):
    """ A Node combines an input server with a queue and a list of handlers """

    def __init__(self, port=50000):
        super(Node, self).__init__()
        self.daemon = True  # Makes the thread exit when the main program exits

        # TODO pick another port if the first one is already bound
        # TODO add the handler and acts lists implementations (think about the semantics and abstractions)
        # TODO make Node be a thread or use its own thread

        # A queue to place incoming messages until they are handled
        self.queue = Queue()
        self.data = Data()

        # Add the put method of the message_queue as callback to the server
        self.server = SocketServer(port, self.data.message_queue.put)

        # handlers are functions that accept the messages from the queue as input
        self.handlers = []

        self.running = True
        self.server.start()

    """
    def add_to_queue(self, message):
        print("Node received: " + message)
        self.messageQueue.put(message)
    """

    def add_handler(self, func):
        self.handlers.append(func)

    def run(self):

        while self.running:
            try:
                # Waits for 3 seconds, otherwise throws `Queue.Empty`
                next_item = self.data.message_queue.get(True, 3)
            except queue.Empty:
                next_item = None

            # Passes the next queue item to all the registered handlers (TODO should I clone the message?)
            if next_item is not None:
                for h in self.handlers:
                    h(next_item)


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


