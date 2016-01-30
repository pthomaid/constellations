
import time
import queue
from queue import Queue
from threading import Thread
from random import randint

from . import config
from constellations.socket_transport import SocketTransport


class Data:

    def __init__(self):
        self.me = {}
        self.peers = {}
        self.peer_set = []

class Node:
    """ A Node combines an input server with a queue and a list of handlers """

    def __init__(self):
        # TODO pick another port if the first one is already bound
        # TODO add the handler and acts lists implementations (think about the semantics and abstractions)
        # TODO make Node be a thread or use its own thread

        # A queue to place incoming messages, decouples the server from the handling
        self.message_queue = Queue()

        # Add the put method of the message_queue as callback to the server
        self.transport = SocketTransport()
        self.data = Data()
        #if(self.transport.host == ""):
        #    self.data.me['address'] = ["localhost", self.transport.port]
        #else:
        self.data.me['address'] = [self.transport.host, self.transport.port]
            
        # Handlers handle the incoming messages
        self.handlers = []

        # Acts are functions run in separate threads, associated with this node and its data
        self.acts = []

        self.running = True

        t = Thread(target=self.queue_consumer)
        t.daemon = True
        t.start()
        
        self.transport.receive(self.message_queue.put)

    def add_handler(self, func):
        # TODO check if func supports the message argument (is this possible?)
        self.handlers.append(func)

    def add_act(self, func):
        # TODO check if func supports the data argument (is this possible?)
        t = Thread(target=func, args=(self,))
        t.daemon = True
        t.start()
        self.acts.append(t)

    def stop(self):
        # TODO safely stop server and all threads
        self.running = False

    def queue_consumer(self):
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
                    h(self, next_item)


if __name__ == "__main__":

    def myhandler1(message):
        print("My handler1 received: " + message)

    def myhandler2(message):
        print("My handler2 received: " + message)

    def greetings_sender(context, data):
        i = 0
        while True:
            SocketClient.send("localhost", data.me['address'][1], "lodpsdppsdpsdf" + str(i))
            i += 1
            time.sleep(2)

    n = Node(port=5003)
    n.add_handler(myhandler1)
    n.add_handler(myhandler2)
    n.add_act(greetings_sender)

    import sys
    time.sleep(1)
    input("Press Enter to continue...")
    sys.exit()


