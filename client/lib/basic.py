import transport

#TODO send API key and public key to server
#get all the games
#select a game
#get session key
#set config.session_key,
#subscribe to session key

#filter={'key','value'}
def get_response(key,value):
    while True:
        for response in transport.response:
            if response.has_key(key) and response[key]==value:
                return transport.response.pop(response)
