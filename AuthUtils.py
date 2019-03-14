import random


class UserDB:

    def __init__(self, db=None):
        if db is None:
            self.udict = dict()
        else:
            self.udict = db

        self.tdb = TokenDB()

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

    def verify(self, user, pword):
        if self.udict.contains(user):
            if self.udict[user] == pword:
                return True
            else:
                return False
        else:
            return False

    def is_auth(self):
        self.tdb
        # TODO: FULFILL PRINT COMMANDS BELOW
        print("do a contains then a token check with tdb")

    def auth_user(self):
        self.udict
        print("CHECK UDICT FOR USER IF FOUND GENERATE TOKEN WITH TDB")

    def parse_name(self):
        print("PARSE NAME FROM INC DATA")

    def parse_token(self):
        print("PARSE TOKEN FROM INC DATA")


class TokenDB:

    def __init__(self):
        self.tdb = []

    def gen_token(self, user):
        temptoken = random.randint(100000000, 999999999)
        self.tdb[user] = temptoken
        return temptoken

    def verif_token(self, user, token):
        if user in self.tdb:
            if self.tdb[user] == token:
                return True
            else:
                return False
        else:
            return False

    def remove_token(self, user, token):
        if user in self.tdb:
            if self.tdb[user] == token:
                del self.tdb[user]
