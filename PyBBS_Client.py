import socket

# TODO: HOST/PORT/USER/TOKEN/DATA would be stored in model
HOST = '127.0.0.1'
PORT = 55555

# TODO: ONCE A HOST/PORT IS RECEIVED ATTEMPT CONNECT
cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

cli_sock.connect((HOST, PORT))

# TODO: IF CONNECTION IS SUCCESSFUL PRINT BELOW TO LOG AND FIRE OFF LOGIN SCREEN
if cli_sock:
    print("Connected to " + HOST + " @", PORT)

# TODO: CREATE MESSAGE WITH LOGIN CREDENTIALS AND TRANSMIT

message = "AUT00000000005BrianHELLO FROM THE OTHERSIIIIDDDE!!"
cli_sock.send(message.encode('ascii'))

inc_data = cli_sock.recv(1024)

if inc_data is not None:
    print(inc_data.decode())

# TODO: IF AUTH IS SUCCESSFUL GO TO MENU SCREEN ELSE DISPLAY INVALID LOGIN AND DROP CONNECTION

cli_sock.close()
