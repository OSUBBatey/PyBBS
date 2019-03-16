import random
import csv


class UserDB:

    def __init__(self, db=None):
        if db is None:
            self.udict = dict()
        else:
            self.udict = db
        self.load_db()
        self.tdb = TokenDB()

    def add_user_no_file(self, user, pword):
        if self.contains(user.lower()) is False:
            self.udict[user.lower()] = pword

    def add_user(self, user, pword):
        if self.contains(user.lower()) is False:
            self.udict[user.lower()] = pword
            self.user_to_file(user, pword)

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
            # TODO: CHECK HERE FOR PASSWORD FIGURE OUT FAILURE
            password = self.parse_pword(payload)
            if self.udict[name] == password:
                return self.tdb.gen_token(name)
            else:
                return 000000000

        else:
            # TODO: PROMPT FOR NEW USER IF TIME ALLOWS
            print("User not found!!!")
            print("Creating new user")
            pword = self.parse_pword(payload)
            self.add_user(name, pword)
            # TODO:OTHERWISE CURRENTLY JUST CREATE A NEW USER IF NOT FOUND

            return self.tdb.gen_token(name)

    def parse_name(self, payload):
        name_len = int(payload[12:14])
        end_pos = 14+name_len
        name_out = payload[14:end_pos]
        print("PARSE NAME FROM INC DATA")
        return name_out

    def parse_token(self, payload):
        print("PARSE TOKEN FROM INC DATA")
        return 000000000

    def parse_pword(self, payload):
        name_len = int(payload[12:14])
        end_pos = 14+name_len
        pword_out = payload[end_pos:]
        print("PARSE NAME FROM INC DATA")
        return pword_out

    def user_to_file(self, uname, pword):
        file = open("ulist.csv", "a+")
        file.write(uname + "," + pword + "\n")
        file.close()

    def load_db(self):
        try:
            file = open("ulist.csv", "r")
            csv_reader = csv.reader(file, delimiter=',')
            count = 0
            for row in csv_reader:
                if count == 0:
                    count = 1
                    pass
                else:
                    self.add_user_no_file(row[0], row[1])
        except IOError:
            file = open("ulist.csv", "a+")
            file.write("User,Pass\n")
            pass


class TokenDB:

    def __init__(self):
        self.tdb = {}

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
