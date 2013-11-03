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

def new_game_server(user_json):
    user = User(json.dumps(user_json))
    server = GameServer()
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
    user = session.query(User).filter(User.api_key == api_key).first()
    game_client = session.query(GameClient).filter(GameClient.user == user).first()
    if game_client:
        return game_client
    game_server = session.query(GameServer).filter(GameServer.user_id == user.id).first()
    if game_server:
        return game_server
    return None

def get_user_from_shared_key(shared_key):
    user = session.query(User).filter(User.shared_key == shared_key).first()
    game_client = session.query(GameClient).filter(GameClient.user == user).first()
    if game_client:
        return game_client
    game_server = session.query(GameServer.filter(GameServer.user == user)).first()
    if game_server:
        return game_server
    return None