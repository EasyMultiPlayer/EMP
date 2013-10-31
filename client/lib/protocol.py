import config
import transport
import user_layer
from basic import get_response
import threading

# step 1
def send_API_key():
    transport.data_request_with_response.append({'action':'REQUEST_GAMES','api_key':config.API_KEY})
    data=get_response('action','RESPONSE_GAMES')
    select_game(data['games'])

def select_game(games):
    session_key=user_layer.select_game(games)
    if session_key==-1:
        transport.data_request_with_response.append({'action':'NEW_GAME','api_key':config.API_KEY})

    else:
        transport.data_request_with_response.append({'action':'SELECT_GAME','api_key':config.API_KEY,'session_key':session_key})

    # should have 'session_key':'asdcasdc'
    data=get_response('action','RESPONSE_SESSION_KEY')
    # now game is set
    config.SESSION_KEY=data['session_key']

    #TODO subscribe to session key