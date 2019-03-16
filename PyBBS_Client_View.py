import tkinter as tk
from tkinter import messagebox


class ServConnFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.label1 = tk.Label(self, text="Enter the Host Address and Port Number of the PyBBS"
                                          " Server You Wish To Connect To ", wraplength=320)
        self.label1.pack()

        self.host_label = tk.Label(self, text="Host:").place(x=30, y=39)

        self.port_label = tk.Label(self, text="Port:").place(x=30, y=59)

        self.host_entry = tk.Entry(self)
        self.host_entry.pack()

        self.port_entry = tk.Entry(self)
        self.port_entry.pack()

        self.close_button = tk.Button(self, text="Connect", command=self.connect2server)
        self.close_button.pack(anchor='s')

    def swap_frame(self):
        self.master.swap_frame(LoginFrame)

    def connect2server(self):
        # Get info from entry fields
        self.get_info()

        # Attempt to connect to server
        if self.master.server_connect():
            # On success, swap to login screen
            messagebox.showinfo("Success!!!", "Connection to " + self.master.model.get_host() + " established")
            self.swap_frame()
        else:
            messagebox.showinfo("Failure!!!", "Connection to " + self.master.model.get_host() + " failed")

    def get_info(self):
        # Get Host Address and add to model
        self.master.model.set_host(self.host_entry.get())

        # Get Connection Port and add to model
        self.master.model.set_port(self.port_entry.get())


class LoginFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.label1 = tk.Label(self, text="Enter Your Username and Password", wraplength=320)
        self.label1.pack()
        self.label2 = tk.Label(self, text="User will be created if it does not exist")
        self.label2.pack()

        self.user_label = tk.Label(self, text="User:").place(x=0, y=43)

        self.pword_label = tk.Label(self, text="Pass:").place(x=0, y=66)

        self.user_entry = tk.Entry(self)
        self.user_entry.pack()

        self.pword_entry = tk.Entry(self)
        self.pword_entry.pack()

        self.close_button = tk.Button(self, text="Login", command=self.login2server)
        self.close_button.pack(anchor='s')

    def swap_frame(self):
        self.master.swap_frame(ServConnFrame)

    def get_info(self):
        # Get User Name
        self.master.model.set_user(self.user_entry.get())

        # Get Password
        self.master.model.set_pword(self.pword_entry.get())

    def login2server(self):
        # TODO: AUTHORIZE USER
        self.get_info()
        self.master.auth_user()
