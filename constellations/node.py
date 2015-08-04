
import time
from queue import Queue

from .basics.socketClientServer import SocketServer
from .basics.socketClientServer import SocketClient


class Node:
    """ A Node combines an input server with a queue and a list of handlers """

    def __init__(self, port=50000):

        # TODO pick another port if the first one is already bound
        # TODO add the handler and acts lists implementations (think about the semantics and abstractions)
        # TODO make Node be a thread or use its own thread

        # A queue to place incoming messages until they are handled
        self.messageQueue = Queue()
        self.server = SocketServer(port, self.add_to_queue)

        # handlers are functions that accept the messages from the queue as input
        self.handlers = []

        self.server.start()

    def add_to_queue(self, message):
        print("Node received: " + message)
        self.messageQueue.put(message)

    def add_handler(self, func):
        self.handlers.append(func)


if __name__ == "__main__":

    n = Node()

    SocketClient.send("localhost", 50000, "lodpsdppsdpsdf")

    import sys
    time.sleep(1)
    input("Press Enter to continue...")
    sys.exit()


