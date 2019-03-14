class BBSDb:

    def __init__(self, Name):
        self.name = Name
        file = open(Name+".txt", "a+")
        file.write("DBName = " + Name)
        file.write("\nStartup Message ---------\n")
        file.close()

    def write(self, message):
        file = open(self.name+".txt", "a")
        file.write(message+"\n")
        file.close()

    def read(self, csock):
        file = open(self.name+".txt", "rb")
        print("Beginning Transfer!!!")
        curr = file.read(1024)
        while curr:
            csock.send(curr)
            curr = file.read(1024)
        file.close()
        print("File Transmission Complete!!!")
