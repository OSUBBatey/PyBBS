import glob
import datetime
import os
DEFAULT = "default"
MAXSIZE = 1024


class BBSDb:

    def __init__(self):
        # TODO: CHANGE THIS TO BE A LOGFILE
        self.name = DEFAULT
        self.name_list = []
        self.active_db = DEFAULT
        file = open(DEFAULT+".txt", "a+")
        file.write("PyBBS Server Log\n")
        file.write("Starting Server ---------\n")
        date = str(datetime.datetime.now())
        file.write(date + "\n")
        file.close()
        self.generate_db_list()

    def write(self, message):
        file = open(self.name+".txt", "a")
        file.write(message+"\n")
        file.close()

    def read(self, csock):
        # Open File and Get File Size
        file = open(self.name+".txt", "rb")

        # Begin Transfer
        print("Beginning Transfer!!!")
        curr = file.read(1024)
        while curr:
            csock.send(curr)
            curr = file.read(1024)
        file.close()
        print("File Transmission Complete!!!")

    def set_active_db(self):
        print("SET ACTIVE DB")

    def generate_db_list(self):
        print("use glob to search local directory")
        if os.path.isdir('./UserDBStore'):
            temp_list = glob.iglob('./UserDbStore/*.txt')
            for user in temp_list:
                self.name_list.append(user[:-4])
        else:
            os.mkdir('UserDBStore')

    def generate_db(self):
        print("generate new database")

    def contains(self, name):
        print("check DB list for name")

    def get_msg_size(self, file):
        size = os.stat(file)
        return size.st_size
