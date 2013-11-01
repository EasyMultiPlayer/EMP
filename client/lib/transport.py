import zmq
import json
import traceback
import config
import time
from lib import logging

data_request_with_response = []
data_push = []
data_pull = [] # this is populated by the server
data_sub = []
reply = None
response = {}

# this is used only in the initial stages
def server_request_response():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    #socket.connect("tcp://127.0.0.1:6001")
    #socket.bind("tcp://*:" + config.PORT_REPC)
    socket.connect("tcp://"+config.HOST+":"+config.PORT_REPC)
    print "tcp://"+config.HOST+":"+config.PORT_REPC

    while True:
        try:
            # TODO send everything in a batch
            for index in range(0,len(data_request_with_response)):
                data=data_request_with_response.pop(index)
                data['time']=time.time()
                socket.send(json.dumps(data))
                response_data=socket.recv()
                response.append(json.loads(response_data),"[REQ]")
        except:
            traceback.print_exc()


# this is used later on
def server_push():
    context = zmq.Context()
    socket = context.socket(zmq.PUSH)

    socket.connect("tcp://"+config.HOST+":"+config.PORT_PUSH)
    print "tcp://"+config.HOST+":"+config.PORT_PUSH

    while True:
        try:
            for data in data_push:
                data['time']=time.time()
                socket.send(json.dumps(data))
                logging.debug(json.dumps(data),"[PUSH]")
                data_push.remove(data)

        except:
            traceback.print_exc()

def server_pull():
    context = zmq.Context()
    socket = context.socket(zmq.PULL)

    socket.connect("tcp://"+config.HOST+":"+config.PORT_PULL)
    print "tcp://"+config.HOST+":"+config.PORT_PULL

    while True:
        try:
            # TODO do we need to convert it to json from string ?? O.o
            data=socket.recv()
            logging.debug(json.loads(data),"[PULL]")
            data_pull.append(json.loads(data))

        except:
            traceback.print_exc()

# DONT start this right in the beginning coz u dont know what is the session key of the game instance
# todo see whether client has to subscribe to many session keys
def server_subscribe(session_key):
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://"+config.HOST+":"+config.PORT_SUB)
    print "tcp://"+config.HOST+":"+config.PORT_SUB

    socket.setsockopt(zmq.SUBSCRIBE,session_key)
    while True:
        try:
            data=socket.recv()
            logging.debug(json.loads(data),"[SUBSCRIBE]")
            data_sub.append(json.loads(data))
        except:
            traceback.print_exc()


