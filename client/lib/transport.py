import zmq
import threading
import config

data_request_with_response = []
data_request_without_response = []
reply = None
response = []


def send_request_with_response():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    #socket.connect("tcp://127.0.0.1:6001")
    socket.bind("tcp://*:" + config.PORT_REPC)
    #socket.connect("tcp://127.0.0.1:5600")

    #for i in range(10):
    #    msg = "msg %s" % i
    #    socket.send(msg)
    #    print "Sending", msg
    #    msg_in = socket.recv()
    #    print msg_in

    while True:
        for part in data_request_with_response:
            # TODO make sure that it sends proper data
            thread_send_and_get = threading.Thread(target=send_and_get, args=(socket, part,))
            thread_send_and_get.start()
            #socket.send(part)


def send_and_get(socket, part):
    socket.send(part)
    response.append(socket.recv())


def send_request_without_response():
    #TODO here waiting for response must happen in a thread
    pass
