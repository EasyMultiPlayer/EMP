import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy import ForeignKey

Base=declarative_base()

class User(Base):
	__tablename__='users'

	id = Column(Integer, primary_key=True)
	user_json=Column(String)
	#api_key=Column(Integer,ForeignKey("api_keys.id"))
	api_key=relationship("APIKey", order_by="APIKey.id", backref="users")
	# like localhost:8000
	address=Column(String)
	time=Column(TIMESTAMP)

	def __init__(self,user_json,address):
		self.user_json=user_json
		self.api_key=api_key
		self.address=address

	def info(self):
		return json.loads(self.user_json)

class GameServer(User):
	__tablename__="game_server"
	def __init__(self,user_json,apiKey):
		super().__init__(user_json,apiKey)

class GameClient(User):
	__tablename__="game_client"
	server_shared_key=Column(String)

	def __init__(self,user_json,apiKey,server_shared_key):
		super().__init__(user_json,apiKey)
		self.server_shared_key=server_shared_key

class APIKey(Base):
	__tablename__="api_keys"
	id = Column(Integer, primary_key=True)
	private_key=Column(String)
	shared_key=Column(String)

	def __init__(self,private_key,shared_key):
		self.private_key=private_key
		self.shared_key=shared_key

class Session(Base):
	__tablename__="session"
	key=Column(String)
	user=relationship("User", order_by="users.id", backref="session_keys")

	def __init__(self,key,user,ip):
		self.key=key
		self.user=user

class Log(Base):
	__tablename__="logs"
	id=Column(Integer, primary_key=True)
	key=Column(String)
	value=Column(String)

	def __init__(self,key="Debug",value):
		self.key=key
		self.value=value

class Game(Base):
	__tablename__="games"
	id=Column(Integer,primary_key=True)
	# info should have all the necessary stuffs about the game for clients to connect
	data=Column(String)
	session_key=relationship("Game", order_by="session_keys.id", backref="games")

	def __init__(self,data):
		self.data=data