import threading
import zmq
import config
import logging, status

# request response server
def startREP():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # listening to client
    socket.bind("tcp://*:" + config.PORT_REPC)

    while True:
        try:
            string = socket.recv()

            print logging.error(string)
            # TODO do something with data here
            # TODO create a thread and send it to the game server
            thread = threading.Thread(target=sendToGameServer, args=(string,))
            thread.start()

            socket.send(status.SUCCESS)
        except:
            socket.close()

def sendToGameServer(args):
    # TODO
    print args