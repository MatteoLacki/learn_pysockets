import socket
import sys

port = int(sys.argv[1])
HEADERSIZE = 10

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), port))

full_msg = ""
new_msg = True
while True:
    msg = s.recv(16)

    if new_msg:
        print(f"new message length: {msg[:HEADERSIZE]}")
        msglen = int(msg[:HEADERSIZE])
        new_msg = False
    
    full_msg += msg.decode("utf-8")

    if len(full_msg) - HEADERSIZE == msglen:
        print(f"Full message: {full_msg[HEADERSIZE:]}")
        full_msg = ""
        new_msg = True
