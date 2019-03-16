import tkinter as tk
import socket
from PyBBS_Client_View import ServConnFrame
from PyBBSClient_Model import ClientModel


class PyClientCtrl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.root = self
        self.title("PyBBS Client")
        self.geometry('400x150')
        self.model = ClientModel()
        self.frame = ServConnFrame(self)
        self.frame.pack()

    def run(self):
        self.root.mainloop()

    def swap_frame(self, frame):
        self.frame.pack_forget()
        self.frame = frame(self)
        self.frame.pack()

    def server_connect(self):
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.model.set_socket(cli_sock)
            self.model.get_socket().connect((self.model.get_host(), self.model.get_port()))
            # If connection successful , update model , return true
            # cli_sock.connect((self.model.get_host(), self.model.get_port()))
            print("Connected to " + self.model.get_host() + " @", self.model.get_port())

            return True

        except socket.error:
            return False

    def auth_user(self):

        # Get socket from model
        cli_sock = self.model.get_socket()
        name_len = len(self.model.user)
        if name_len < 10:
            temp = str(name_len)
            name_len = '0' + temp

        # Create Authorization message using model information
        message = "AUT" + '000000000' + name_len + self.model.user + self.model.pword

        try:
            cli_sock.send(message.encode('ascii'))
            result = cli_sock.recv(1024)
            return self.parse_token(result)

        except socket.error:
            print("ERROR SENDING/RECEIVING AUTHORIZATION TO/FROM CLIENT!!!")
            return False

    def parse_token(self, data):
        if data[:3] == 'ATS':
            tok_out = data[3:]
            self.model.set_token(tok_out)
            return True
        else:
            return False


if __name__ == '__main__':
    c = PyClientCtrl()
    c.run()
