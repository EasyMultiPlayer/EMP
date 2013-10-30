import threading
import zmq
import json
import config
import traceback
import logging, status
import copy

data_push = []
data_pub = {} # this should have 'session_key':'<data_to_be_pushed>' dictionary

# request response server
def server_request_response():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # listening to client
    socket.bind("tcp://*:" + config.PORT_REPC)

    while True:
        try:
            string = socket.recv()

            print logging.debug(string)
            # TODO do something with data here
            # TODO create a thread and send it to the game server
            thread = threading.Thread(target=sendToGameServer, args=(string,))
            thread.start()

            socket.send(status.SUCCESS)
        except:
            socket.close()

def server_pull():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)

    # listening to client
    socket.bind("tcp://*:" + config.PORT_PULL)

    while True:
        try:
            string = socket.recv()

            print logging.debug(string)
            thread = threading.Thread(target=sendToGameServer, args=(string,))
            thread.start()

        except:
            socket.close()

# this is used later on
def server_push():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)

    socket.bind("tcp://*:" + config.PORT_PUSH)

    while True:
        try:
            for data in data_push:
                socket.send(json.dumps(data))
                data_push.remove(data)

        except:
            traceback.print_exc()

def server_publish():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)

    socket.bind("tcp://*:" + config.PORT_PUB)
    while True:
        data_queue=copy.deepcopy(data_pub)
        for session_key in data_queue:
            socket.send(session_key + " " + data_queue[session_key])
            del(data_pub[session_key])

def sendToGameServer(args):
    # TODO
    pass