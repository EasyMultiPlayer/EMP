from lib import db

db.setup()
#user={'fname':'alse','lname':'ambusher','game':'aoe'}
#db.new_game_server(user)
#db.session.commit()

user={'fname':'gamer2','lname':'pro2'}
db.new_game_client(user,"104568c23cca3bfd93220a60acde852b")
db.session.commit()
