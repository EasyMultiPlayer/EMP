from lib.transport import Transport

client = Transport()
client.start()

i={"1":"a","2":"b"}
import time
while True:
    client.data_push.append(i)
    time.sleep(1)