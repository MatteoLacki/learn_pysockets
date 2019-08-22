import socket
import select
import errno
import sys

PORT = int(sys.argv[1])
HEADER_LEN = 10
# IP = "127.0.0.1"
IP = socket.gethostname()

my_username = input("Username: ")
client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_s.connect((IP, PORT))
client_s.setblocking(False) # the receive will not block.

username  = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LEN}}".encode('utf-8')
client_s.send(username_header + username) # not in the while, because user set only once

while True:
    message = input(f"{my_username} > ")
    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LEN}}".encode('utf-8')
        client_s.send(message_header + message)

    try:
        while True: # receiving things
            username_h = client_s.recv(HEADER_LEN)
            if not username_h:
                print('Connection closed by the server.')
                sys.exit()
            username_len = int(username_h.decode('utf-8').strip())
            username = client_s.recv(username_len).decode('utf-8')
            message_h = client_s.recv(HEADER_LEN)
            message_len = int(message_h.decode('utf-8').strip())
            message = client_s.recv(message_len).decode('utf-8')
            
            print(f"{username} > {message}")

    except IOError as e:
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print("Reading error", str(e))
            sys.exit()
        continue

    except Exception as e:
        print('General error', str(e))
        sys.exit()
