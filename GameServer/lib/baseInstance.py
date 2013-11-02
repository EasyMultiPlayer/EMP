import random

class BaseInstance():
    # array of user shared keys
    users=[]
    status=''
    def __init__(self,session_key):
        self.session_key=session_key
        # this is used only till it gets a session key
        self.id=str(random.random())

    # add user to instance
    def join_instance(self,client_shared_key):
        self.users.append(client_shared_key)

    def leave_instance(self,client_shared_key):
        self.users.remove(client_shared_key)
        # todo test this
        if len(self.users) == 0:
            self.status='removed'