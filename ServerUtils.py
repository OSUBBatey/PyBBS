import types
import selectors
import tkinter as tk
toaster_out = tk.Tk()
MSG_SIZE = 1024


def queue_socket(sock, p_list):
    cli_sock, addr = sock.accept()
    print('connection established @', addr)
    cli_sock.setblocking(False)
    payload = types.SimpleNamespace(addr=addr, data_in="", data_out="", sel=p_list, tok=000000000)
    event = selectors.EVENT_READ
    p_list.register(cli_sock, event, data=payload)


def process_current(s_key, e_mask, db, udb, p_list):

    if e_mask is selectors.EVENT_READ:
        receive(s_key, db, udb, p_list)
    elif e_mask is selectors.EVENT_WRITE:
        send(s_key, db)


def receive(sock_key, active_db, user_db, p_list):  # TODO: SPLIT THIS UP TO A SEND FUNCTION FOR OUTGOING
    cli_conn = sock_key.fileobj
    inc_data = None
    try:
        inc_data = cli_conn.recv(MSG_SIZE)
    except IOError:
        print("Socket Receive Failure!!!!")
        exit()   # Halt on Closed

    # Check incoming operation
    action = parse_header(inc_data.decode())

    if action == 'A':
        data = inc_data.decode()
        # Store token with socket package
        sock_key.data.tok = user_db.auth_user(data)

        # Ensure Token is in the proper range else failure has occurred
        if sock_key.data.tok >= 100000000:
            # Generate ACK msg for client
            msg = gen_auth_ack(sock_key.data.tok)
            cli_conn.send(msg.encode("ascii"))
        else:
            # Generate FAIL msg for client
            msg = gen_fail_ack(sock_key.data.tok)
            cli_conn.send(msg.encode("ascii"))
    elif action == 'X':
        print("Closing Connection")
        p_list.unregister(cli_conn)
        cli_conn.close()

    else:
        # Check if user is logged in , then verify authorization token
        if is_logged_in(sock_key.data.tok) and user_db.is_auth(inc_data.decode()):

            # perform operations
            # TODO: SIMPLIFY THIS AND SPLIT TO READ/WRITE COMMANDS IN SELECTOR
            if action == 'W':
                # TODO: NEED TO DILINEATE BETWEEN PUBLIC / PRIVATE DATA (USE HEADER?)
                # TODO: STRIP WRITE COMMAND OUT OF THE DB
                msg_in = inc_data.decode()
                name = parse_name(msg_in)
                name = name + ' : '
                msg_in = name + strip_header(msg_in)
                active_db.write(msg_in)
            elif action == 'R':
                active_db.read(cli_conn)
            else:
                    print("INVALID OPERATION REQUEST")
        else:
            print('Invalid Credentials!!!!')
            # authorize failed .. tell client to check credential and resend request


def send(sock_key, active_db):
    # TODO:READ FROM DB
    print()


def parse_header(payload):
    plntxt = payload[:3]
    if plntxt == 'AUT':
        print("AUTHORIZATION REQUEST")
        return 'A'
    elif plntxt == 'WDB':
        print("CALL WRITE TO DATABASE")
        return 'W'
    elif plntxt == 'RDB':
        print("CALL READ FUNCTION ON DB")
        return 'R'
    elif plntxt == 'XXX':
        print("CALL READ FUNCTION ON DB")
        return 'X'
    else:
        print("INVALID OPCODE IN HEADER")
        return 'INV'


def is_logged_in(token):
    if token < 100000000:
        return False
    else:
        return True


def gen_auth_ack(token):
    msg_out = 'ATS' + str(token)
    return msg_out


def gen_fail_ack(token):
    msg_out = 'ATF' + str(token)
    return msg_out


def parse_name(payload):
    assert len(payload) >= 14, "Invalid Data Header!!!"
    name_len = int(payload[12:14])
    end_pos = 14+name_len
    name_out = payload[14:end_pos]
    return name_out


def strip_header(payload):
    end_marker = payload.find('EOM')
    if end_marker > -1:
        msg_out = payload[end_marker+3:]
    else:
        print("Invalid Header!!!!")
        msg_out = payload

    return msg_out
