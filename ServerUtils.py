import types
import selectors
import tkinter as tk
toaster_out = tk.Tk()
MSG_SIZE = 1024


def queue_socket(sock, p_list):
    cli_sock, addr = sock.accept()
    print('connection established @', addr)
    cli_sock.setblocking(False)
    payload = types.SimpleNamespace(addr=addr, data_in="", data_out="", sel=p_list)
    event = selectors.EVENT_READ
    p_list.register(cli_sock, event, data=payload)


def process_current(s_key, e_mask, db, tdb):

    if e_mask is selectors.EVENT_READ:
        receive(s_key, db, tdb)
    elif e_mask is selectors.EVENT_WRITE:
        send(s_key, db)


def receive(sock_key, active_db, token_db):
    cli_conn = sock_key.fileobj
    inc_data = cli_conn.recv(MSG_SIZE)

    if inc_data:
        if token_db.is_auth(inc_data):
            action = parse_header(inc_data)
            if action == 'W':
                active_db.write(inc_data.decode()[3:])
                m_out = "Message Written!!!"
                cli_conn.send(m_out.encode("ascii"))
            elif action == 'R':
                # TODO:Prepare read
                active_db.read(cli_conn)
            else:
                print("INVALID OPERATION REQUEST")
        else:
            token_db.auth_user(inc_data)
        #  msg = inc_data.decode()

        # if msg[:2] == 'EK':
        #    m_out = "MAIL MO FO!!!!"
        #    cli_conn.send(m_out.encode("ascii"))

        # elif msg[:2] == 'DS':
            # test = tk.Label(toaster_out, text=inc_data.decode()[2:])
            # test.pack()
            # toaster_out.mainloop()
            #   print(inc_data.decode()[2:])


def send(sock_key, active_db):
    # TODO:READ FROM DB
    print()


def parse_header(payload):
    plntxt = payload.decode()[:3]
    if plntxt == 'WDB':
        print("CALL WRITE TO DATABASE")
        print("RETURN SUCCESS")
        return 'W'
    elif plntxt == 'RDB':
        print("CALL READ FUNCTION ON DB")
        print("FIND DATA AND SEND IT BACK")
        return 'R'
    else:
        print("INVALID HEADER FORMAT")
        # TODO: make possible to read/write in one message by parsing through data
        # TODO: make auth command for access/login authorization
        return 'INV'
