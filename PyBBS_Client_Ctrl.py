import tkinter as tk
import time
import socket
from PyBBS_Client_View import ServConnFrame
from PyBBSClient_Model import ClientModel
import os


class PyClientCtrl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.root = self
        self.title("PyBBS Client")
        self.geometry('400x150')
        self.model = ClientModel()
        self.frame = ServConnFrame(self)
        self.frame.pack()
        self.tframe = tk.Frame()
        self.tframe.destroy()

    def run(self):
        self.root.mainloop()

    def swap_frame(self, frame):
        self.frame.pack_forget()
        self.frame = frame(self)
        self.frame.pack()

    def gen_txt_frame(self, frame):
        if not self.tframe.winfo_exists():
            self.tframe = frame(self)
            self.tframe.pack()

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

        # Create Authorization message using model information
        action = "AUT"
        message = self.create_message(action)

        try:
            # Send Aut Message
            cli_sock.send(message.encode('ascii'))
            result = cli_sock.recv(1024)
            # Check if valid token has been returned
            return self.parse_token(result.decode())

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

    def srv_rd_req_pub(self):
        # Get socket from model
        cli_sock = self.model.get_socket()

        # Create Read Request Message
        action = "RDB"
        message = self.create_message(action)
        result = b''

        # Send Read Request To Server
        try:
            # Send Message
            cli_sock.send(message.encode('ascii'))

        except socket.error:
            print("ERROR SENDING/RECEIVING AUTHORIZATION TO/FROM CLIENT!!!")
            # TODO: CLOSE SOCKET AND SHUTDOWN ON ERROR
            exit()
        # Set time out to release socket when file transfer complete (REBUILD THIS LATER)
        cli_sock.settimeout(.5)
        while True:
            try:
                data = cli_sock.recv(1024)
            except socket.timeout:
                # Restore Blocking to Socket
                cli_sock.settimeout(None)
                return result
            # Accumulate data
            result += data

    def create_message(self, req):
        name_len = len(self.model.user)
        if name_len < 10:
            temp = str(name_len)
            name_len = '0' + temp
        if int(self.model.get_token()) < 100000000:
            token = "000000000"
        else:
            token = str(self.model.get_token())
        # Create server request using model information
        return req + token + name_len + self.model.get_user() + self.model.get_pword()

    def get_msg_size(self, file):
        size = os.stat(file)
        return size.st_size


if __name__ == '__main__':
    c = PyClientCtrl()
    c.run()
