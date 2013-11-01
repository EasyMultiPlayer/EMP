import zmq
import json
import traceback
import config
import time
import threading
from lib import logging

class Transport():

    data_push = []
    data_sub = []
    response = {}

    def __init__(self):
        self.threads=[threading.Thread(target=self.push_server)]

    def start(self):
        for thread in self.threads:
            thread.start()

    def subscribe(self,key):
        thread=threading.Thread(target=self.subscribe_server,args=(key,))
        thread.start()
        self.threads.append(thread)

    def push_server(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)

        for port in config.PORT_PUSH:
            socket.connect("tcp://"+config.HOST+":"+port)

        while True:
            try:
                for data in self.data_push:
                    data['time']=time.time()
                    logging.debug(json.dumps(data),"[PUSH]")
                    socket.send(json.dumps(data))
                    self.data_push.remove(data)

            except:
                traceback.print_exc()

    # DONT start this right in the beginning coz u dont know what is the session key of the game instance
    # todo see whether client has to subscribe to many session keys
    def subscribe_server(self,key):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://"+config.HOST+":"+config.PORT_SUB)

        socket.setsockopt(zmq.SUBSCRIBE,key)
        while True:
            try:
                data=socket.recv()
                logging.debug(json.loads(data),"[SUBSCRIBE]")
                self.data_sub.append(json.loads(data))
            except:
                traceback.print_exc()


