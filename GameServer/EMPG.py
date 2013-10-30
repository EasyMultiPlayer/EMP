from lib import transport
import threading

# Add all threads which have to be run to this array
threads = [threading.Thread(target=transport.server_request_response),
           threading.Thread(target=transport.server_push),
           threading.Thread(target=transport.server_pull)]

# start all servers
for thread in threads:
    thread.start()

for i in range(0, 10000):
    transport.data_push.append({str(i) + 'alse': str(i)})


#transport.data_request_with_response['test1']="testa"
#transport.data_request_with_response['test2']="testb"
#while True:
#    if transport.response.has_key('test1'):
#        print "Got response", transport.response['test1']
#        del(transport.response['test1'])
#        break
#while True:
#    if transport.response.has_key('test1'):
#        print "Got response", transport.response['test1']
#        del(transport.response['test1'])
#        break