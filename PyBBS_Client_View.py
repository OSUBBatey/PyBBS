import tkinter as tk
from tkinter import messagebox
from tkinter import StringVar
from tkinter import OptionMenu
from tkinter.tix import ScrolledWindow
from tkinter import Text


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
        # Swap to User Choice
        self.master.swap_frame(UserChoiceFrame)

    def get_info(self):
        # Get User Name
        self.master.model.set_user(self.user_entry.get())

        # Get Password
        self.master.model.set_pword(self.pword_entry.get())

    def login2server(self):
        self.get_info()
        test = self.master.auth_user()
        if test:
            messagebox.showinfo("Success!!!", "Logged in as: " + self.master.model.get_user())
            self.swap_frame()
        else:
            messagebox.showinfo("Failure!!!", "Invalid Password!!! Please Try Again!!!")


class UserChoiceFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        # Option Box Actions
        self.options = [
            "Please Select an Option",
            "Read Public DataBase",
            "Write To Public DataBase",
            "Logout and Exit"
        ]
        self.var_select = StringVar(master)
        self.ovar = StringVar(master)
        self.ovar.set(self.options[0])
        self.sideWindow = tk.Frame()

        self.obox = OptionMenu(master, self.ovar, *self.options, command=self.set_dropdown_value)
        self.obox.pack()

        self.close_button = tk.Button(self, text="Exit", command=self.quit)
        self.close_button.pack(side=tk.BOTTOM)

        self.testbutton = tk.Button(self, text="Launch Selection", command=self.execute_dropdown_action)
        self.testbutton.pack()

    def set_dropdown_value(self, value):
        self.var_select = value

    def get_dropdown_value(self):
        return self.var_select

    def execute_dropdown_action(self):
        action = self.get_dropdown_value()
        if action == self.options[1]:
            # Action 1 : Read Public MessageBoard
            rcv_file = self.master.srv_rd_req_pub()
            file = open("test.txt", 'w')
            file.write(rcv_file.decode())
            file.close()
            self.disp_txt_win()
        elif action == self.options[2]:
            # TODO: WRITE TO PUB DB (CALL FROM CTRL)
            return 2
        elif action == self.options[3]:
            # TODO: CLOSE SOCKET/LOGOUT AND EXIT PROGRAM
            return 3

    def disp_txt_win(self):
        self.master.gen_txt_frame(RdTextFrame)


class RdTextFrame(tk.Frame):

    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.frame = tk.Toplevel(master)
        self.frame.wm_title("Public Message Board")

        self.frame.scroll = tk.Scrollbar(self.frame)

        with open("test.txt", 'r') as file:
            self.frame.tbox = Text(self.frame, wrap=tk.WORD, yscrollcommand=self.frame.scroll.set)
            self.frame.tbox.insert(tk.INSERT, file.read())
            self.frame.tbox.config(state=tk.DISABLED)

        self.frame.close_button = tk.Button(self.frame, text="Close", command=self.frame.destroy)
        self.frame.scroll.config(command=self.frame.tbox.yview)
        self.frame.scroll.pack(side="right", fill="y")
        self.frame.tbox.pack(side="left", fill="both", expand=True)
        self.frame.close_button.pack(side="bottom", anchor='s')

        self.frame.transient(master)
        self.frame.grab_set()
        master.wait_window(self.frame)
