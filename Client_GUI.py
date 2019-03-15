import tkinter as tk


class ServConnFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.connect_button = tk.Button(self, text="Connect", command=master.set_uname)
        self.connect_button.pack()

        self.swap_button = tk.Button(self, text="Swap", command=self.swap_frame)
        self.swap_button.pack()

        self.close_button = tk.Button(self, text="Close", command=self.quit)
        self.close_button.pack()

    def swap_frame(self):
        self.master.swap_frame(LoginFrame)


class LoginFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.login_button = tk.Button(self, text="Accept", command=master.set_uname)
        self.login_button.pack()

        self.swap_button = tk.Button(self, text="Swap", command=self.swap_frame)
        self.swap_button.pack()

        self.close_button = tk.Button(self, text="Exit", command=self.quit)
        self.close_button.pack()

    def swap_frame(self):
        self.master.swap_frame(ServConnFrame)

