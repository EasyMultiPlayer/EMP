from lib.transport import Transport
from lib import protocol

client = Transport()
protocol.init(client)

import time
while True:
    client.send(query={"1":"a","2":"b"})
    time.sleep(1)