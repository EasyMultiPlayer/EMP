from lib.transport import Transport
import threading

client_transport = Transport()
server_transport = Transport()

client_transport.start()
