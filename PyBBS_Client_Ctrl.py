import tkinter as tk
from Client_GUI import ServConnFrame
from PyBBSClient_Model import ClientModel


class PyClientCtrl(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.root = self
        self.title("PyBBS")
        self.geometry('250x150')
        self.model = ClientModel()
        self.frame = ServConnFrame(self)
        self.frame.pack()

    def run(self):
        self.root.title("PyBBS")
        self.root.mainloop()

    def swap_frame(self, frame):
        self.frame.pack_forget()
        self.frame = frame(self)
        self.frame.pack()

    def set_uname(self):
        print("Greetings!")
        self.model.set_user('Brian')


if __name__ == '__main__':
    c = PyClientCtrl()
    c.run()
