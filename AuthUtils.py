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

    def is_auth(self, payload):
        name = self.parse_name(payload)
        token = self.parse_token(payload)
        if name in self.udict:
            return self.tdb.verif_token(name, token)
        else:
            print("Must Login for Authorization!")
            return False
        # TODO: FULFILL PRINT COMMANDS BELOW

    def auth_user(self, payload):
        name = self.parse_name(payload)
        if name in self.udict:
            return self.tdb.gen_token(name)
        else:
            print("User not found!!!")
            # TODO:FIGURE OUT FAILURE RETURN
            return 000000000

    def parse_name(self, payload):
        name_len = int(payload[12:14])
        end_pos = 14+name_len
        name_out = payload[14:end_pos]
        print("PARSE NAME FROM INC DATA")
        return name_out

    def parse_token(self, payload):
        print("PARSE TOKEN FROM INC DATA")
        return 000000000


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
