import threading
import zmq
import copy
import config
import logging

class Transport():
    data_push = []
    data_pub = {} # this should have 'session_key':'<data_to_be_pushed>' dictionary

    def __init__(self):
        self.threads=[threading.Thread(target=self.server_publish)]

        for port in config.PORT_PULL:
            self.threads.append(threading.Thread(target=self.server_pull,args=(port,)))

    def start(self):
        for thread in self.threads:
            thread.start()

    def server_pull(self,port):
        context = zmq.Context()
        socket = context.socket(zmq.PULL)

        # listening to client
        socket.bind("tcp://*:" + port)

        while True:
            try:
                string = socket.recv()

                print logging.debug(string,'[PULL:'+port+']')
                thread = threading.Thread(target=sendToGameServer, args=(string,))
                thread.start()

            except:
                socket.close()

    def server_publish(self):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)

        socket.bind("tcp://*:" + config.PORT_PUB)
        while True:
            data_queue=copy.deepcopy(self.data_pub)
            for session_key in data_queue:
                socket.send(session_key + " " + data_queue[session_key])
                del(self.data_pub[session_key])

def sendToGameServer(args):
    # TODO
    pass