from lib import db

#db.setup()
user={'name':'alse','game_level':0,'blah':'boo'}
game_state='x-axis,y-axis,gold,wood'
db.create_new_game_server(user,'127.0.0.1',game_state)
db.session.commit()
