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

    def set_uname(self):
        print("Greetings!")
        self.model.set_user('Brian')

    def server_connect(self):
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            cli_sock.connect((self.model.get_host(), self.model.get_port()))
            self.model.socket = cli_sock
            return True
        except socket.error:
            return False


if __name__ == '__main__':
    c = PyClientCtrl()
    c.run()
