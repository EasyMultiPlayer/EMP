import sqlalchemy
import config
from models import *
from sqlalchemy.orm import sessionmaker
import json

engine = sqlalchemy.create_engine("sqlite:///" + config.DB, echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def setup():
    Base.metadata.create_all(engine)


#def save_session(api_key=None, shared_key=None, key=None):
#    if not key:
#        key = keys.session_key_gen()
#
#    session_key=SessionKeys(key)
#    if api_key:
#        user=session.query(User).filter(User.private_key == api_key)
#    else:
#        user=session.query(User).filter(User.shared_key == shared_key)
#
#    session_key.user=user
#    session.add(session_key)
#    session.commit()
#    return session_key

def create_new_game_server(user_json, game_state_params):
    user = User(json.dumps(user_json))
    server = GameServer(game_state_params)
    server.user = user
    session.add(server)
    session.commit()
    return server


def new_game_client(user_json, server_shared_key):
    user = User(json.dumps(user_json))
    client = GameClient(server_shared_key)
    client.user = user
    session.add(client)
    session.commit()
    return client

def get_user_from_api_key(api_key):
    user = session.query(User).filter(User.api_key == api_key)
    game_client = session.query(GameClient).filter(GameClient.user == user)
    if game_client:
        return game_client
    game_server = session.query(GameServer.filter(GameServer.user == user))
    if game_server:
        return game_server
    return None

def get_user_from_shared_key(shared_key):
    user = session.query(User).filter(User.shared_key == shared_key)
    game_client = session.query(GameClient).filter(GameClient.user == user)
    if game_client:
        return game_client
    game_server = session.query(GameServer.filter(GameServer.user == user))
    if game_server:
        return game_server
    return None