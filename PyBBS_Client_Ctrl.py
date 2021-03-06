import tkinter as tk
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
            self.tframe = frame(self)

    def server_connect(self):
        # Client Socket
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # Create socket connections and store in model
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
        # Token is first 3 characters
        if data[:3] == 'ATS':
            tok_out = data[3:]
            self.model.set_token(tok_out)
            return True
        else:
            return False

    def srv_rd_req_pub(self):  # Send read request for public board to server
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
                break
            # Accumulate data
            result += data

        # TODO: Implement Error Checking
        # TODO: TXTVAR1
        file = open("test.txt", 'w')
        file.write(result.decode())
        file.close()

    def srv_wrt_req_pub(self, data):  # Send write request for public board to server
        # Get socket from model
        cli_sock = self.model.get_socket()

        # Create Read Request Message
        action = "WDB"
        message = self.create_message(action)
        message = self.add_end_of_msg(message)

        # Prepend Data with Request Header
        message += data

        # Send Write Request To Server
        try:
            # Send Message
            cli_sock.sendall(message.encode('ascii'))
            return True

        except socket.error:
            print("ERROR SENDING/RECEIVING AUTHORIZATION TO/FROM CLIENT!!!")
            # TODO: CLOSE SOCKET ON ERROR
            return False

    def create_message(self, req):  # Create Request Header where 'req' is the 3 letter OpCode for an action
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

    def add_end_of_msg(self, payload):
        return payload + 'EOM'

    def get_msg_size(self, file):
        size = os.stat(file)
        return size.st_size

    def close_connection(self):
        cli_sock = self.model.get_socket()
        message = 'XXX'
        cli_sock.send(message.encode('ascii'))
        print("Closing Connection")
        cli_sock.close()


if __name__ == '__main__':
    c = PyClientCtrl()
    c.run()
