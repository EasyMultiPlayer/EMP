from lib.transport import Transport

client = Transport()
client.start()

i={"1":"a","2":"b"}
import time
while True:
    client.send(query=i)
    time.sleep(1)