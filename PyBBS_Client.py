import socket

HOST = '127.0.0.1'
PORT = 55555

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cli_sock.connect((HOST, PORT))

message = "RDBHELLO FROM THE OTHERSIIIIDDDE!!"
cli_sock.send(message.encode('ascii'))

inc_data = cli_sock.recv(1024)

if inc_data is not None:
    print(inc_data.decode())

cli_sock.close()
