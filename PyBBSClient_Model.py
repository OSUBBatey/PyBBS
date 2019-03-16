class ClientModel:
    def __init__(self):
        self.pword = None
        self.user = None
        self.host = None
        self.port = None
        self.msgin = None
        self.msgout = None
        self.socket = None

    def set_pword(self, data_in):
        self.pword = data_in

    def get_pword(self):
        return self.pword

    def set_user(self, data_in):
        self.user = data_in

    def get_user(self):
        return self.user

    def set_host(self, data_in):
        # TODO: IMPLEMENT ERROR CHECKING
        self.host = data_in

    def get_host(self):
        return self.host

    def set_port(self, data_in):
        # TODO: IMPLEMENT ERROR CHECKING
        self.port = int(data_in)

    def get_port(self):
        return self.port

    def set_msgin(self, data_in):
        self.msgin = data_in

    def get_msgin(self):
        return self.msgin

    def set_msgout(self, data_in):
        self.msgout = data_in

    def get_msgout(self):
        return self.msgout

    def set_socket(self, data_in):
        self.socket = data_in

    def get_socket(self):
        return self.socket
