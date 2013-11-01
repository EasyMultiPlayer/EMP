import zmq
import json
import traceback
import config
import time
import threading
from lib import logging
from res import actions


class Transport():
    data_push = []
    data_sub = []
    response = {}

    def __init__(self):
        self.threads = [
            threading.Thread(target=self.push_server),
            threading.Thread(target=self.alive)
        ]

    # this starts all the servers
    def start(self):
        for thread in self.threads:
            thread.start()

    # call this method to subscribe to a new key
    def subscribe(self, key):
        thread = threading.Thread(target=self.subscribe_server, args=(key,))
        thread.start()
        self.threads.append(thread)

    # call this to push to the api server
    def send(self, query={}, action=None, api=False, shared=False, session=False, server_shared=False):
        query['time'] = time.time()
        if action:
            query['action'] = action
        if api:
            query['api_key'] = config.API_KEY
        if shared:
            query['shared_key'] = config.SHARED_KEY
        if session:
            query['session_key'] = config.SESSION_KEY
        if server_shared:
            query['server_shared_key'] = config.SERVER_SHARED_KEY

        self.data_push.append(json.dumps(query))

    # this keeps sending packet to server to tell that it is alive
    def alive(self):
        while True:
            self.send(action=actions.alive, server_shared=True)
            time.sleep(config.ALIVE_PULSE)

    def push_server(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUSH)

        for port in config.PORT_PUSH:
            socket.connect("tcp://" + config.HOST + ":" + port)

        while True:
            try:
                for data in self.data_push:
                    print logging.debug(data, "[PUSH]")
                    socket.send(data)
                    self.data_push.remove(data)

            except:
                traceback.print_exc()

    # DONT start this right in the beginning coz u dont know what is the session key of the game instance
    # todo see whether client has to subscribe to many session keys
    def subscribe_server(self, key):
        context = zmq.Context()
        socket = context.socket(zmq.SUB)
        socket.connect("tcp://" + config.HOST + ":" + config.PORT_SUB)

        socket.setsockopt(zmq.SUBSCRIBE, key)
        while True:
            try:
                data = socket.recv()
                logging.debug(json.loads(data), "[SUBSCRIBE]")
                self.data_sub.append(json.loads(data))
            except:
                traceback.print_exc()
