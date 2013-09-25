import zmq

def sendReq():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:6001")
    #socket.connect("tcp://127.0.0.1:5600")

    for i in range(10):
        msg = "msg %s" % i
        socket.send(msg)
        print "Sending", msg
        msg_in = socket.recv()
        print msg_in

if __name__=="__main__":
    sendReq()