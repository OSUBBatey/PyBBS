import random


class UserDB:

    def __init__(self, db=None):
        if db is None:
            self.udict = dict()
        else:
            self.udict = db

    def add_user(self, user, pword):
        if self.udict.contains(user) is False:
            self.udict[user] = pword

    def contains(self, uname):
        if uname in self.udict:
            return True
        else:
            return False

    def update_user(self, user, pword):
        if self.udict.contains(user):
            self.udict[user] = pword

    def rm_user(self, user):
        if self.udict.contains(user):
            del self.udict[user]
        else:
            print("User not found!!!")

    def verify(self,user,pword):
        if self.udict.contains(user):
            if self.udict[user] == pword:
                return True
            else:
                return False
        else:
            return False


class TokenDB:

    def __init__(self):
        self.tdb = []

    def gen_token(self,user):
        temptoken = random.randint(100000000,999999999)
        self.tdb[user] = temptoken
        return temptoken

    def verif_token(self, user, token):
        if user in self.tdb:
            if self.tdb[user]==token:
                return True
            else:
                return False
        else:
            return False

    def remove_token(self, user, token):
        if user in self.tdb:
            if self.tdb[user] == token:
                del self.tdb[user]
