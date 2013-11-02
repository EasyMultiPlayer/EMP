from res import actions, status
import db
# when client queries for available games
# TODO attach this to transport
def response_client_request_games(api_key):
    client=db.get_user_from_api_key(api_key)
    # TODO ask game server to give which game to give