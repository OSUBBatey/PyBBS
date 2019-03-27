import socket
import selectors
from ServerUtils import queue_socket
from ServerUtils import process_current
from PyBBS_DB_Log_Utils import BBSDb
from AuthUtils import UserDB

# The method in the function below (get_local_ip) adapted from :
# https://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
# All credit for the initial creation goes to user : Jamieson Becker


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # dummy address to find default route
        s.connect(('10.255.255.255', 1))
        out = s.getsockname()[0]
    except IOError:
        # use loop-back in case of failure
        out = '127.0.0.1'
    finally:
        s.close()
    return out


user_prompt = input("Would you like to Auto-detect the local server IP? (y or n) : ")
if user_prompt is 'y':
    print("Automatically detecting local IP!!!")
    HOST = get_local_ip()
elif user_prompt is 'n':
    HOST = input("Enter the IP address you wish to use: ")
else:
    print("Unknown command! Defaulting to Auto-detect!!!")
    print("Automatically detecting local IP!!!")
    HOST = get_local_ip()


print("Local Address is: ", str(HOST))
print("Using this as the server address!!!")
print()
PORT = int(input("Please designate a Port # to use: "))
PORTALT = 44444
MAX_CON = 1
stop_loop = False
port_list = selectors.DefaultSelector()
master_DB = BBSDb()
auth_DB = UserDB()

# create the server's main socket
serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to the host and designated port
try:
    serv_sock.bind((HOST, PORT))

    print('Server Started!!!!')
    print('listening @ ', (HOST, PORT))
except socket.error:
    serv_sock.bind((HOST, PORTALT))

    print('Server Started!!!!')
    print('listening @ ', (HOST, PORTALT))

# set socket as a non blocking listening socket
serv_sock.listen(MAX_CON)
serv_sock.setblocking(False)

# register socket in selector
port_list.register(serv_sock, selectors.EVENT_READ, data=None)

# handle client connections
# TODO: Fix Exit Point For Loop (stop_loop)
while True:
    sock_event_list = port_list.select(timeout=None)
    for s_key, event_mask in sock_event_list:
        if s_key.data is None:
            queue_socket(s_key.fileobj, port_list)

        else:
            process_current(s_key, event_mask, master_DB, auth_DB, port_list)
    if stop_loop:
        break

serv_sock.close()

