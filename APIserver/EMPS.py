import time
import threading
import zmq
import config
from lib import logging

def startREP():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    socket.connect(config.HOST+":"+config.PORT_REP)

    while True:
        string  = socket.recv()

        # TODO create a thread and send it to the game server
        print("Received request: [%s]\n" % (string))

        time.sleep(1)

        socket.send("World")


