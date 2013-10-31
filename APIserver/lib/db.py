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


def save_session(private_key=None, shared_key=None, key=None):
    if not key:
        key = keys.session_key_gen()

    session_key=SessionKeys(key)
    if private_key:
        user=session.query(User).filter(User.private_key == private_key)
    else:
        user=session.query(User).filter(User.shared_key == shared_key)

    session_key.user=user
    session.add(session_key)
    session.commit()
    return session_key

def create_new_user(user_json, address):
    user=User(json.dumps(user_json),address)
    session.add(user)
    # session.commit()
    return user

def create_new_game_server(user_json,address,game_state_params):
    user=create_new_user(user_json,address)
    server=GameServer(game_state_params)
    server.user=user
    session.add(server)
    # session.commit()