from lib import transport
import threading

thread = threading.Thread(target=transport.startREP)
thread.start()