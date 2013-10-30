import zmq
import json
import traceback
import config

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
                socket.send(json.dumps(data))
                # now response[key] will have the required data
                key,val=data
                response[key]=socket.recv()
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
                socket.send(json.dumps(data))
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
            data_pull.append(json.loads(socket.recv()))

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
            data_sub.append(json.loads(socket.recv()))
        except:
            traceback.print_exc()


