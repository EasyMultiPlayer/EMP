import config
import transport
import user_layer
from basic import get_response
import threading
from res import constants

# step 1
def send_API_key():
    transport.data_request_with_response.append({'action':constants.REQUEST_GAMES,'api_key':config.API_KEY})
    data=get_response('action',constants.RESPONSE_GAMES)
    select_game(data['games'])

def select_game(games):
    session_key=user_layer.select_game(games)
    if session_key==-1:
        transport.data_request_with_response.append({'action':constants.NEW_GAME,'api_key':config.API_KEY})

    else:
        transport.data_request_with_response.append({'action':constants.SELECT_GAME,'api_key':config.API_KEY,'session_key':session_key})

    # TODO if he cant connect to it u have to request again
    # should have 'session_key':'asdcasdc'
    data=get_response('action',constants.RESPONSE_SESSION_KEY)
    # now game is set
    config.SESSION_KEY=data['session_key']

    # subscribe to session key
    thread=threading.Thread(target=transport.server_subscribe, args=(config.SESSION_KEY,))
    thread.start()