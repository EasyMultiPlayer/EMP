import threading
import zmq
import json
import config
import traceback
import logging, status

data_push = []

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

    socket.connect("tcp://"+config.HOST+":"+config.PORT_PUSH)
    print "tcp://"+config.HOST+":"+config.PORT_PUSH

    while True:
        try:
            for data in data_push:
                socket.send(json.dumps(data))
                data_push.remove(data)

        except:
            traceback.print_exc()

def server_publish():
    pass

def sendToGameServer(args):
    # TODO
    pass