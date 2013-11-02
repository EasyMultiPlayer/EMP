import threading
import zmq
import copy
import config
import logging
import time
import json
from res import actions
import db
from basic import data_filter


class Transport():
    logs = []
    data_pub = {} # this should have 'session_key':'<data_to_be_pushed>' dictionary

    def __init__(self):
        self.threads = [
            threading.Thread(target=self.publish),
            threading.Thread(target=self.batch_logger)
        ]

        for port in config.PORT_PULL:
            self.threads.append(threading.Thread(target=self.pull, args=(port,)))

    def start(self):
        for thread in self.threads:
            thread.start()

    def send(self, query, action, key):
        query['time'] = time.time()
        if action:
            query['action'] = action

        self.data_pub[key] = json.dumps(query)

    # keeps logging in a batch
    def batch_logger(self):
        while True:
            for log in self.logs:
                # TODO
                self.logs.remove(log)
            time.sleep(5)

    def pull_processor(self, data):
        _action = data['actions']

        # from game_server or client
        if _action == actions.connect:
            print logging.debug("Connect " + data['api_key'], "[Info]")

        # from client
        elif _action == actions.get_games:
            # TODO if client doesnt exist then raise error
            client = db.get_user_from_api_key(data['api_key'])
            print logging.debug(actions.get_games, '[Info]')
            self.send({'shared_key': client.user.shared_key}, action=actions.get_games, key=client.server_shared_key)

        # from game server
        elif _action == actions.game_list:
            # replace server shared key with client shared key
            data['shared_key'] = data['client_shared_key']
            key = data['client_shared_key']
            # remove that field
            data = data_filter(data, ['client_shared_key', ])
            # publish to that key
            self.send(data, action=actions.game_list, key=key)

        # from client select game
        elif _action == actions.select_game:
            # TODO
            pass

        # from client new game
        elif _action == actions.new_game:
            #TODO
            pass

    def pull(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)

        # listening to client
        socket.bind("tcp://*:" + port)

        while True:
            string = socket.recv()
            #print logging.debug(string, '[PULL:' + port + ']')
            thread = threading.Thread(target=self.pull_processor, args=(json.loads(string),))
            thread.start()

    # TODO make this multi threaded
    def publish(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)

        socket.bind("tcp://*:" + config.PORT_PUB)
        while True:
            data_queue = copy.deepcopy(self.data_pub)
            for session_key in data_queue:
                socket.send(session_key + " " + data_queue[session_key])
                del (self.data_pub[session_key])
