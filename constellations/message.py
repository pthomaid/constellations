
import time
import json
import queue
from queue import Queue
from threading import Thread
from random import randint


def parse(s):
    # TODO Handle cases when the parsing goes wrong (exception, default values)
    d = json.loads(s)
    m = Message(d)
    return m


def compose(m):
    if isinstance(m, Message):
        return json.dumps(m.to_dict())
    else:
        s = json.dumps(m)
        return s


# TODO subclass dict?
class Message:
    """
    Describes a simple message with a sender address, a receiver address and a contained message
    """

    def __init__(self, d=None):
        if d is not None:
            self.from_dict(d)
        else:
            self.from_address = ['', -1]
            self.to_address = ['', -1]
            self.message = {}

    def from_dict(self, d):
        self.from_address = d['from']
        self.to_address = d['to']
        self.message = d['message']

    def to_dict(self):
        d = {}
        d['from'] = self.from_address
        d['to'] = self.to_address
        d['message'] = self.message
        return d