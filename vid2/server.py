import socket
import time

HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 0)) #0 will select the first open port.
print("ip {}\tport {}".format(*s.getsockname()))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print(f"Connection from {address} established.")
    msg = "Welcome to the server!"
    msg = f"{len(msg):<{HEADERSIZE}}" + msg
    clientsocket.send(bytes(msg, "utf-8"))
    # clientsocket.close()

    while True:
        time.sleep(1)
        msg = f"The time is: {time.time()}"
        print(f'Sending "{msg}" to {address[1]}.')
        msg = f"{len(msg):<{HEADERSIZE}}" + msg
        clientsocket.send(bytes(msg, "utf-8"))