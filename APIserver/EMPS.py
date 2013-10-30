from lib import transport
import threading

threads = [threading.Thread(target=transport.server_request_response),
           threading.Thread(target=transport.server_pull),
           threading.Thread(target=transport.server_push),
           threading.Thread(target=transport.server_publish)
           ]

for thread in threads:
    thread.start()