import config
import user_layer
from res import actions

# step 1
def init(transport):
    # get game list
    transport.send(action=actions.get_games,api=True)
    data=transport.get_response(action=actions.game_list)

    # TODO check this
    # user selects a game
    key = user_layer.select_game(data['games'])

    if key == "-1":
        # want to create a new game
        transport.send(action=actions.new_game, api=True)

    elif key in data['games'].keys():
        # connect to a game which already exists
        transport.send(query={'game':key ,},action=actions.select_game,api=True)

    # get the session key of the game instance
    session_key=transport.get_response(action=actions.game_session)
    config.SESSION_KEY=session_key['session_key']

    # subscribe to the session key of the game
    transport.subscribe(session_key['session_key'])
