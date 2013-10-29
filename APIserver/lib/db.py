import sqlalchemy
import config
from models import *
from sqlalchemy.orm import sessionmaker
import json

engine=sqlalchemy.create_engine("sqlite:///"+config.DB, echo = False)
Session=sessionmaker(bind=engine)
session=Session()

def setup():
    Base.metadata.create_all(engine)


def save_session_key_to_db(user, ip=None, key=None):
    #TODO
    pass

def create_new_user(user_json, address):
    user=User(json.dumps(user_json),address)
    session.add(user)
    #session.commit()
    return user

def create_new_game_server(user_json,address,game_state_params):
    user=create_new_user(user_json,address)
    server=GameServer(game_state_params)
    server.user=user
    session.add(server)
    #session.commit()