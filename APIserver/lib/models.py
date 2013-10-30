import json
import keys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_json = Column(String)
    #api_key=Column(Integer,ForeignKey("api_keys.id"))
    private_key = Column(String)
    shared_key = Column(String)
    # like localhost:8000
    address = Column(String)
    time = Column(TIMESTAMP)

    def __init__(self, user_json, address):
        self.user_json = user_json
        self.address = address
        self.private_key, self.shared_key = keys.api_key_gen()

    def info(self):
        return json.loads(self.user_json)


class GameServer(Base):
    __tablename__ = "game_server"
    id = Column(Integer, primary_key=True)
    user_id=Column(Integer,ForeignKey(User.id))
    user = relationship(User,uselist=False)
    game_state_params = Column(String)

    def __init__(self, game_state_params="[]"):
        self.game_state_params = game_state_params
        #super(GameServer, self).__init__(user_json, apiKey)


class GameClient(Base):
    __tablename__ = "game_client"
    id = Column(Integer, primary_key=True)
    server_shared_key = Column(String)
    user_id=Column(Integer,ForeignKey(User.id))
    user = relationship(User,uselist=False)

    def __init__(self, server_shared_key):
        self.server_shared_key = server_shared_key


#class APIKey(Base):
#    __tablename__ = "api_keys"
#    id = Column(Integer, primary_key=True)
#    private_key = Column(String)
#    shared_key = Column(String)
#
#    def __init__(self, private_key, shared_key):
#        self.private_key = private_key
#        self.shared_key = shared_key


class SessionKeys(Base):
    __tablename__ = "session_keys"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    user_id=Column(Integer,ForeignKey(User.id))
    user = relationship(User,uselist=False)

    def __init__(self, key, user, ip):
        self.key = key
        self.user = user


class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True)
    key = Column(String)
    value = Column(String)

    def __init__(self, value, key="Debug"):
        self.key = key
        self.value = value


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    # info should have all the necessary stuffs about the game for clients to connect
    data = Column(String)
    session_id=Column(Integer,ForeignKey(SessionKeys.id))
    session_key = relationship(SessionKeys,uselist=False)

    def __init__(self, data):
        self.data = data
