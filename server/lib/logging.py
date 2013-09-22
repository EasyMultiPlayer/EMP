import config
import time
"""
To be done:
1
debug(key,message)
return <time> : <key> : <message>
2
error(message)
return <time> : ERROR : <message>
and write in config.ERROR_LOG
3
access(ip,type)
write <time>: ip:type in config.ACCESS_LOG
4
log(array of arguments)
write <time>: args in config.LOG
"""
def getCurrentTime():
	return time.strftime("%d-%m-%Y %H:%M:%S")

def debug(key,message):
	return getCurrentTime()+":"+key+":"+message

