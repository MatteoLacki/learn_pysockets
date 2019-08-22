import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 12342))
s.listen(5)


while True:
	clientsocket, address = s.accept()
	print(f"Connection from {address} established.")
	clientsocket.send(bytes("Welcome to the server!", "utf-8"))
	clientsocket.close()