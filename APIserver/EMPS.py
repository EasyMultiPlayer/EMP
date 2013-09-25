import time
import threading
import zmq
import config
from lib import transport, logging, status

# request response server
def startREP():
    context = zmq.Context()
    socket = context.socket(zmq.REP)

    # listening to client
    socket.bind("tcp://*:"+config.PORT_REPC)

    while True:
        try:
            string  = socket.recv()

            print logging.debug(string)
            # TODO create a thread and send it to the game server
            thread=threading.Thread(target=transport.sendToGameServer,args=(string,))
            thread.start()

            socket.send(status.SUCCESS)
        except KeyboardInterrupt:
            socket.close()
        except:
            socket.send(status.ERROR)

if __name__=="__main__":
    startREP()


